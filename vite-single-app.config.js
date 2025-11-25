import path from "path";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import frappeui from "frappe-ui/vite";

const appName = process.env.VITE_APP_NAME || 'qrpay';
const basePath = `/assets/custom_erp/frontend/${appName}/`;

export default defineConfig({
	plugins: [
		frappeui(),
		vue()
	],
	base: basePath,
	build: {
		chunkSizeWarningLimit: 1500,
		outDir: `custom_erp/public/frontend/${appName}`,
		emptyOutDir: true,
		target: "es2015",
		sourcemap: false,
		minify: false,
		rollupOptions: {
			input: path.resolve(__dirname, `${appName}/index.html`),
			output: {
				entryFileNames: `assets/${appName}-[hash].js`,
				chunkFileNames: 'assets/[name]-[hash].js',
				assetFileNames: 'assets/[name]-[hash].[ext]',
				manualChunks: {
					vendor: ['vue', 'vue-router'],
					ui: ['frappe-ui'],
				},
			},
		},
	},
	resolve: {
		alias: {
            "@shared": path.resolve(__dirname, "shared"),
			"tailwind.config.js": path.resolve(__dirname, "tailwind.config.js"),
		},
	},
	optimizeDeps: {
		include: ["feather-icons", "showdown", "highlight.js/lib/core", "interactjs"],
	},
})

