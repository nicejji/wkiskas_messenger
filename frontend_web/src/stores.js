import { writable } from "svelte/store";

export const me = writable(null)
export const recipient = writable(null)
export const chat = writable(null)
export const ws = writable(null)
export const messages = writable(null)