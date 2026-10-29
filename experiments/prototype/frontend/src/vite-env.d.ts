// Environment variables read by the page (.env file, VITE_ prefix)
interface ImportMetaEnv {
  readonly VITE_RUNTIME_URL: string;
  readonly VITE_BACKEND_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
