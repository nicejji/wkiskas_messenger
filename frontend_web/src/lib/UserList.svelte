<script>
    import {fade, scale} from 'svelte/transition';

    import {createEventDispatcher} from "svelte";
    import {recipient} from "../stores.js";

    const dispatch = createEventDispatcher()

    let recipientValue;
    recipient.subscribe(v => recipientValue = v)

    let targetUsername = ''
    let found_users = []

    async function getUsers() {
        const res = await fetch('/users?q=' + targetUsername, {headers: {Authorization: 'Bearer ' + localStorage.getItem('token')}})
        if (res.ok) {
            found_users = await res.json()
        }
    }
</script>

<div in:scale out:fade class="flex flex-col box-border gap-2">
    <input spellcheck="false" type="text" class="rounded-lg p-1 text-center bg-slate-900 outline-none w-full"
           placeholder="Search user" bind:value={targetUsername}
           on:input={()=>{getUsers()}}>
    <div in:scale out:fade class="flex flex-col w-full gap-1">
        {#if targetUsername}
            <p>Search results:</p>
            {#each found_users as u (u.id)}
                <div class="bg-slate-600 rounded-lg p-2 flex"
                     on:click={() => {recipient.set(u); dispatch('chat', ''); targetUsername=''}}>{u.username}</div>
            {/each}
        {/if}
    </div>
</div>