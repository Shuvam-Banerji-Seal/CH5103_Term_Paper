import { defineConfig } from 'vite';

// public/ holds symlinks to the scene fonts and to video/build/program.json (written by video/tools/program.py)
export default defineConfig({ server: { fs: { allow: ['..', '../..'] } }, preserveSymlinks: false });
