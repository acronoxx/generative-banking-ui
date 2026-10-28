// Environment variables read by the page (.env file, VITE_ prefix)
interface ImportMetaEnv {
  readonly VITE_RUNTIME_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
