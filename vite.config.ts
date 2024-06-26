import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tsconfigPaths from 'vite-tsconfig-paths'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())
  const protocol = mode == 'development' ? 'http' : 'https'
  const backendHost = env.VITE_BACKEND_HOST || '127.0.0.1:5000'
  return {
    plugins: [react(), tsconfigPaths()],
    root: './src/frontend',
    envDir: '../../',
    base: mode == 'development' ? '/' : '/dist',
    server: {
      host: true,
      port: 5001,
      strictPort: true,
      watch: {
        ignored: [
          './src/*.py',
          './src/**/*.py'
        ]
      }
    },
    define: {
      BACKEND_HOST: JSON.stringify(protocol + '://' + backendHost)
    }
  }
})
