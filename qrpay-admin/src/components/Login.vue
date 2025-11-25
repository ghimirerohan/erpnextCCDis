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
        <Button type="submit" :loading="session.login.loading" variant="solid"
          >Login</Button
        >
        <Button
          v-if="canUseBiometric"
          type="button"
          variant="subtle"
          @click="loginWithBiometric"
          class="mt-2"
        >
          <template #prefix>
            <FeatherIcon name="lock" class="w-4 h-4" />
          </template>
          Login with Biometrics
        </Button>
      </form>
    </Card>

    <Dialog
      v-model="showBiometricModal"
      :options="{
        title: 'Enable Biometric Login',
        actions: [
          {
            label: 'Enable',
            variant: 'solid',
            onClick: enableBiometric
          },
          {
            label: 'Not Now',
            variant: 'subtle',
            onClick: skipBiometric
          }
        ]
      }"
    >
      <template #body-content>
        <p class="text-gray-600">
          Would you like to enable biometric login (Touch ID / Face ID) for faster access next time?
        </p>
      </template>
    </Dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted, computed } from "vue"
import { session, setNavigationCallbacks, getNavigationCallbacks } from "../../../shared/data/session"
import { FeatherIcon, ErrorMessage, Card, Input, Button, Dialog } from "frappe-ui"

const email = ref("")
const password = ref("")
const showPassword = ref(false)
const errorMessage = ref("")
const passwordWrapperRef = ref<HTMLElement | null>(null)
const passwordToggleStyle = ref({ top: "2rem" })

const showBiometricModal = ref(false)
const savedEmail = ref("")
const savedPassword = ref("")
const canUseBiometric = ref(false)

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
					// @ts-ignore
					transform: 'translateY(-50%)'
				}
			}
		}
	}, 100)

    // Check if we can offer biometric login
    // @ts-ignore
    if (window.PasswordCredential && localStorage.getItem('biometric_enabled')) {
        canUseBiometric.value = true
        // Optional: Auto-trigger? Maybe too intrusive.
    }
})

const togglePasswordVisibility = () => {
	showPassword.value = !showPassword.value
}

const getErrorMessage = (error: any) => {
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

async function submit(e: any) {
	errorMessage.value = ""
	
	// Clear any previous errors
	if (session.login.error) {
		session.login.error = null
	}

    // Intercept success callback
    const originalCallbacks = getNavigationCallbacks()
    let loginSuccessful = false

    // Temporarily override callback to prevent auto-redirect
    setNavigationCallbacks({
        onLoginSuccess: (route: any) => {
            loginSuccessful = true
            // Do not redirect yet
        },
        onLogoutSuccess: originalCallbacks.onLogoutSuccess
    })

	try {
		const formData = e?.target ? new FormData(e.target) : null
        const usr = email.value || (formData ? formData.get("email") as string : "")
        const pwd = password.value || (formData ? formData.get("password") as string : "")

		await session.login.submit({
			email: usr,
			password: pwd,
		})

        if (loginSuccessful) {
            // Check if we should prompt for biometric
            // Only if PasswordCredential is supported and not already enabled (or maybe always ask if not enabled?)
            // @ts-ignore
            if (window.PasswordCredential && !localStorage.getItem('biometric_enabled')) {
                savedEmail.value = usr
                savedPassword.value = pwd
                showBiometricModal.value = true
            } else {
                // Proceed to redirect
                setNavigationCallbacks(originalCallbacks) // Restore
                if (originalCallbacks.onLoginSuccess) {
                    originalCallbacks.onLoginSuccess("/")
                } else {
                    window.location.reload()
                }
            }
        }

	} catch (error) {
		console.error("Login error:", error)
        setNavigationCallbacks(originalCallbacks) // Restore on error
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

async function enableBiometric() {
    try {
        // @ts-ignore
        if (window.PasswordCredential) {
            // @ts-ignore
            const cred = new PasswordCredential({
                id: savedEmail.value,
                password: savedPassword.value,
                name: savedEmail.value, // Optional: Display name
            });
            await navigator.credentials.store(cred);
            localStorage.setItem('biometric_enabled', 'true');
            canUseBiometric.value = true;
        }
    } catch (e) {
        console.error("Failed to store credential:", e);
    } finally {
        showBiometricModal.value = false;
        proceedLogin();
    }
}

function skipBiometric() {
    showBiometricModal.value = false;
    proceedLogin();
}

function proceedLogin() {
    const originalCallbacks = getNavigationCallbacks()
    if (originalCallbacks.onLoginSuccess) {
        originalCallbacks.onLoginSuccess("/")
    } else {
        window.location.reload()
    }
}

async function loginWithBiometric() {
    try {
        // @ts-ignore
        if (window.PasswordCredential) {
            const cred = await navigator.credentials.get({
                // @ts-ignore
                password: true,
                federated: {
                    providers: ['https://accounts.google.com'] // Optional
                }
            });
            
            // @ts-ignore
            if (cred && cred.type === 'password') {
                // @ts-ignore
                email.value = cred.id;
                // @ts-ignore
                password.value = cred.password;
                // Auto submit
                submit(null);
            }
        }
    } catch (e) {
        console.error("Biometric login failed:", e);
        errorMessage.value = "Biometric login failed. Please use password."
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
