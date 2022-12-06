<script>
    import {scale, fade} from 'svelte/transition'
    import {me, recipient, messages, chat, ws} from "../stores.js";

    let meValue;
    me.subscribe(v => meValue = v)

    const handleLogout = () => {
        me.set(null)
        chat.set(null)
        recipient.set(null)
        ws.set(null)
        messages.set(null)
        localStorage.setItem('token', null)
    }

</script>

{#if meValue}
    <div class="w-full flex flex-row justify-between items-center p-3 max-w-md">
        <span class="text-slate-400 text-xs">Logged as: <span class="font-bold text-white">{meValue.username}</span></span>
        <button class="text-xs text-red-400 p-2 bg-slate-600 rounded-lg" on:click={() => handleLogout()}>Logout</button>
    </div>
{:else}
    <div in:scale out:fade class="bg-white text-slate-800 px-2 rounded-lg font-bold text-2xl flex">
        WKISKAS
    </div>
{/if}