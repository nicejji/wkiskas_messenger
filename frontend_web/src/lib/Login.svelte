<script>
    import {me} from '../stores.js';
    import {fade, scale} from "svelte/transition";

    let error = false
    let username = ''
    let password = ''

    async function tokenAuth() {
        const res = await fetch('/me', {headers: {Authorization: 'Bearer ' + localStorage.getItem('token')}})
        if (res.ok) {
            const user = await res.json()
            me.set(user)
        }
    }

    async function auth() {
        let formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)
        const res = await fetch('/token', {method: 'POST', body: formData})
        if (res.ok) {
            error = false
            const token = (await res.json()).access_token
            localStorage.setItem('token', token)
            await tokenAuth()
        } else {
            error = true
        }
    }

    tokenAuth()
</script>

<div in:scale out:fade class="w-full h-full flex flex-col items-center justify-center gap-2 p-6 max-w-md">
    <p class="font-bold text-3xl">Authorization</p>
    <input class="rounded-lg p-3 text-center bg-slate-900 outline-none w-full" placeholder="Username" type="text"
           bind:value={username}>
    <input class="rounded-lg p-3 text-center bg-slate-900 outline-none w-full" placeholder="Password" type="password"
           bind:value={password}>
    <button class="rounded-lg p-3 bg-cyan-800 font-bold w-full" on:click={()=>{auth()}}>Sign in</button>
    {#if error}
        <p class="text-red-400 text-center text-xs">Incorrect password or user already exists</p>
    {/if}
</div>