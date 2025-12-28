import path from "path";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import frappeui from "frappe-ui/vite";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const appName = process.env.VITE_APP_NAME || 'qrpay';
const basePath = `/assets/custom_erp/frontend/${appName}/`;
const outDir = path.resolve(__dirname, `custom_erp/public/frontend/${appName}`);
const indexHtmlPath = path.resolve(__dirname, `custom_erp/www/${appName}.html`);

export default defineConfig({
	plugins: [
		frappeui({
			lucideIcons: true,
			frappeProxy: true,
			jinjaBootData: true,
			buildConfig: {
				outDir: outDir,
				baseUrl: basePath,
				indexHtmlPath: indexHtmlPath,
				emptyOutDir: true,
				sourcemap: false,
			}
		}),
		vue()
	],
	base: basePath,
	build: {
		chunkSizeWarningLimit: 1500,
		outDir: outDir,
		emptyOutDir: true,
		target: "es2015",
		sourcemap: false,
		minify: false,
		commonjsOptions: {
			include: [/node_modules/],
		},
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
		dedupe: ['vue', 'vue-router', 'nepali-date-converter'],
	},
	optimizeDeps: {
		include: ["feather-icons", "showdown", "highlight.js/lib/core", "interactjs", "nepali-date-converter"],
	},
})

