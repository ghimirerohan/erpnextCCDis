<template>
  <FrappeUIProvider>
    <div class="min-h-screen bg-surface-gray-2">
      <header
        class="sticky top-0 z-10 flex items-center justify-between border-b border-outline-gray-1 bg-white px-4 py-3 shadow-sm"
      >
        <h1 class="text-lg font-semibold text-ink-gray-9">
          {{ currentTitle }}
        </h1>
        <span class="max-w-[45%] truncate text-sm text-ink-gray-6" :title="currentUser">
          {{ currentUser }}
        </span>
      </header>
      <main class="pb-[4.5rem]">
        <router-view />
      </main>
      <nav
        class="fixed inset-x-0 bottom-0 z-10 flex border-t border-outline-gray-1 bg-white pb-[env(safe-area-inset-bottom)] shadow-[0_-1px_0_rgba(0,0,0,0.06),0_-4px_16px_rgba(0,0,0,0.04)]"
        aria-label="Primary"
      >
        <router-link
          v-for="tab in tabs"
          :key="tab.to"
          v-slot="{ href, navigate, isActive, isExactActive }"
          :to="tab.to"
          custom
        >
          <a
            :href="href"
            class="flex flex-1 flex-col items-center gap-1 py-2.5 text-2xs font-medium transition-colors"
            :class="
              tabExactActive(tab, isExactActive, isActive)
                ? 'text-ink-blue-3'
                : 'text-ink-gray-5 hover:text-ink-gray-8'
            "
            @click="navigate"
          >
            <span
              class="flex size-9 items-center justify-center rounded-lg transition-colors"
              :class="
                tabExactActive(tab, isExactActive, isActive) ? 'bg-surface-blue-2' : ''
              "
            >
              <FeatherIcon
                :name="tab.icon"
                class="size-[1.125rem]"
                :stroke-width="2"
              />
            </span>
            {{ __(tab.label) }}
          </a>
        </router-link>
      </nav>
    </div>
  </FrappeUIProvider>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { FrappeUIProvider, FeatherIcon } from 'frappe-ui'

const route = useRoute()
const currentUser =
	typeof window !== 'undefined' && window.session_user
		? window.session_user
		: typeof window !== 'undefined' && window.frappe?.session?.user
			? window.frappe.session.user
			: ''

const tabs = [
	{ to: '/', icon: 'home', label: 'Dashboard', exact: true },
	{ to: '/payment', icon: 'credit-card', label: 'Payment', exact: false },
	{ to: '/credits', icon: 'file-text', label: 'Credits', exact: false },
	{ to: '/close', icon: 'check-circle', label: 'Close Day', exact: true },
]

function tabExactActive(tab, isExactActive, isActive) {
	return tab.exact ? isExactActive : isActive
}

const currentTitle = computed(() => {
	const p = route.path || ''
	if (p === '/' || p === '') return __('My Dashboard')
	if (p.startsWith('/payment')) return __('Record Payment')
	if (p.startsWith('/credits')) return __('Credit History')
	if (p.startsWith('/close')) return __('Day Closing')
	return __('CC Field App')
})
</script>
