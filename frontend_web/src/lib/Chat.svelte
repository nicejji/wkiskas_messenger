<script>
    import {scale, fade} from 'svelte/transition'
    import UserList from "./UserList.svelte";

    import {ws, messages, chat, recipient, me} from "../stores.js";

    let messageInput = '';

    const format_date = (d) => {
        const date = new Date(d)
        return `${date.getDate()}.${date.getMonth() + 1} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
    }

    let recipientValue;
    let meValue;
    let wsValue
    let messagesValue
    let chatValue
    recipient.subscribe(v => recipientValue = v)
    me.subscribe(v => meValue = v)
    ws.subscribe(v => wsValue = v)
    messages.subscribe(v => messagesValue = v)
    chat.subscribe(v => chatValue = v)

    async function set_chat() {
        if (wsValue) {
            chat.set(null)
            messages.set(null)
            wsValue.close()
            ws.set(null)
        }
        const res = await fetch('/create_chat?' + (new URLSearchParams({user_id: recipientValue.id})).toString(), {
            method: 'POST',
            headers: {Authorization: 'Bearer ' + localStorage.getItem('token')}
        })
        if (res.ok) {
            chat.set(await res.json())
        }
        const messages_res = await fetch('/messages?' + (new URLSearchParams({chat_id: chatValue.id})), {headers: {Authorization: 'Bearer ' + localStorage.getItem('token')}})
        if (messages_res.ok) {
            messages.set((await messages_res.json()).sort((a, b) => new Date(a.created) - new Date(b.created)).reverse())
        }
        document.cookie = `token=${localStorage.getItem('token')}`
        const params = new URLSearchParams({chat_id: chatValue.id})
        const new_ws = new WebSocket('wss://' + location.host + '/messenger?' + params.toString())
        new_ws.onmessage = (e) => {
            const message = JSON.parse(JSON.parse(e.data))
            messages.set([message, ...messagesValue])
        }
        ws.set(new_ws)
    }
</script>

<div class="w-full h-full flex flex-col gap-3 box-border max-w-md">
    <UserList on:chat={() => set_chat()}/>
    <div class="w-full flex justify-center items-center gap-2">
        {#if recipientValue}
            <p class="font-bold text-xl">{recipientValue.username}</p>
            <p class="text-xs text-green-200">recipient</p>
        {/if}
    </div>
    <div class="w-full h-full flex flex-col-reverse gap-1 overflow-scroll rounded-lg">
        {#if messagesValue}
            {#if !messagesValue.length}
                <div in:scale out:fade class="w-full h-full flex justify-center items-center">
                    <p class="text-lg text-slate-200">No messages here.</p>
                </div>
            {/if}
            {#each messagesValue as m (m.id)}
                <div in:scale
                     class={"w-full h-fit flex flex-row flex-wrap justify-between text-l p-3 rounded-lg items-center" + ' ' + (meValue.id === m.user_id ? 'bg-cyan-600' : 'bg-slate-600')}>
                    <span class="break-all">{m.content}</span>
                    <span class="text-xs text-slate-200">{format_date(m.created)}</span>
                </div>
            {/each}
        {:else}
            <div in:scale out:fade class="w-full h-full flex justify-center items-center">
                <p class="text-lg text-slate-200">Select chat in menu above.</p>
            </div>
        {/if}
    </div>
    {#if recipientValue}
        <div in:scale out:fade class="w-full flex flex-row gap-2 bg-slate-700 p-3 rounded-lg box-border h-fit">
            <input type="text" class="rounded-lg p-3 bg-slate-800 outline-none w-full" placeholder="Type something..."
                   bind:value={messageInput}>
            <button class="rounded-lg p-3 bg-cyan-400 font-bold w-fit text-gray-700"
                    on:click={() => {wsValue.send(messageInput); messageInput=''}}>Send
            </button>
        </div>
    {/if}
</div>