<template>
  <div class="m-3 flex flex-row items-center justify-center">
    <Card title="Login to your FrappeUI App!" class="w-full max-w-md mt-4">
      <form class="flex flex-col space-y-2 w-full" @submit.prevent="submit">
        <Input
          required
          name="email"
          type="text"
          placeholder="johndoe@email.com"
          label="User ID"
          v-model="email"
        />
        <div class="relative password-field-wrapper" ref="passwordWrapperRef">
          <Input
            required
            name="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="••••••"
            label="Password"
            v-model="password"
            class="pr-10"
          />
          <button
            type="button"
            @click="togglePasswordVisibility"
            class="absolute right-3 text-gray-600 hover:text-gray-800 focus:outline-none flex items-center justify-center transition-colors p-1 z-10 password-toggle-btn"
            :style="passwordToggleStyle"
            :aria-label="showPassword ? 'Hide password' : 'Show password'"
          >
            <FeatherIcon
              :name="showPassword ? 'eye-off' : 'eye'"
              class="w-4 h-4"
            />
          </button>
        </div>
        <ErrorMessage
          v-if="errorMessage"
          :message="errorMessage"
          class="text-red-600 text-sm"
        />
        <Button :loading="session.login.loading" variant="solid"
          >Login</Button
        >
      </form>
    </Card>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted } from "vue"
import { session } from "../data/session"
import { FeatherIcon, ErrorMessage } from "frappe-ui"

const email = ref("")
const password = ref("")
const showPassword = ref(false)
const errorMessage = ref("")
const passwordWrapperRef = ref<HTMLElement | null>(null)
const passwordToggleStyle = ref({ top: "2rem" })

// Clear error when user starts typing
watch([email, password], () => {
	if (errorMessage.value) {
		errorMessage.value = ""
	}
})

// Calculate button position to align with input field
onMounted(() => {
	setTimeout(() => {
		if (passwordWrapperRef.value) {
			const input = passwordWrapperRef.value.querySelector('input[name="password"]') as HTMLElement
			if (input) {
				const wrapperRect = passwordWrapperRef.value.getBoundingClientRect()
				const inputRect = input.getBoundingClientRect()
				const offsetTop = inputRect.top - wrapperRect.top + inputRect.height / 2
				passwordToggleStyle.value = {
					top: `${offsetTop}px`,
					transform: 'translateY(-50%)'
				}
			}
		}
	}, 100)
})

const togglePasswordVisibility = () => {
	showPassword.value = !showPassword.value
}

const getErrorMessage = (error) => {
	// Handle network errors (no internet)
	if (!navigator.onLine) {
		return "No internet connection. Please check your network and try again."
	}

	// Handle fetch errors (network failures)
	if (error instanceof TypeError && error.message.includes("fetch")) {
		return "Unable to connect to server. Please check your internet connection and try again."
	}

	// Handle HTTP errors
	if (error?.httpStatus) {
		if (error.httpStatus === 0 || error.httpStatus >= 500) {
			return "Server error occurred. Please try again later or contact support."
		}
		if (error.httpStatus === 401 || error.httpStatus === 403) {
			return "Invalid User ID or password. Please check your credentials and try again."
		}
		if (error.httpStatus === 404) {
			return "Server not found. Please verify the server URL and try again."
		}
		return `Server error (${error.httpStatus}). Please try again later.`
	}

	// Handle error messages from the API
	if (error?.messages && Array.isArray(error.messages)) {
		const message = error.messages.join(", ")
		if (message.toLowerCase().includes("invalid") || message.toLowerCase().includes("incorrect")) {
			return "Invalid User ID or password. Please check your credentials and try again."
		}
		return message
	}

	if (error?.message) {
		const msg = error.message.toLowerCase()
		if (msg.includes("invalid") || msg.includes("incorrect") || msg.includes("wrong")) {
			return "Invalid User ID or password. Please check your credentials and try again."
		}
		if (msg.includes("network") || msg.includes("fetch") || msg.includes("failed")) {
			return "Network error. Please check your internet connection and try again."
		}
		if (msg.includes("server") || msg.includes("500") || msg.includes("502") || msg.includes("503")) {
			return "Server error occurred. Please try again later or contact support."
		}
		return error.message
	}

	// Handle error object with exc_type
	if (error?.exc_type) {
		return "An error occurred during login. Please try again."
	}

	// Default error message
	return "Login failed. Please check your User ID and password, then try again."
}

async function submit(e) {
	errorMessage.value = ""
	
	// Clear any previous errors
	if (session.login.error) {
		session.login.error = null
	}

	try {
		const formData = new FormData(e.target)
		await session.login.submit({
			email: email.value || formData.get("email"),
			password: password.value || formData.get("password"),
		})
	} catch (error) {
		console.error("Login error:", error)
		errorMessage.value = getErrorMessage(error)
		
		// Also check if session.login has an error
		if (session.login.error) {
			const sessionError = getErrorMessage(session.login.error)
			if (sessionError !== errorMessage.value) {
				errorMessage.value = sessionError
			}
		}
	}
}
</script>

<style scoped>
.password-field-wrapper {
  position: relative;
}

.password-field-wrapper :deep(input[name="password"]) {
  padding-right: 2.75rem !important;
}

.password-toggle-btn {
  position: absolute;
  right: 0.75rem;
  display: flex;
  align-items: center;
  cursor: pointer;
}
</style>
