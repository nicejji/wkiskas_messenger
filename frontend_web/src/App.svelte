<script>
    import './app.css'
    import Login from "./lib/Login.svelte";
    import Chat from "./lib/Chat.svelte";


    const appHeight = () => {
        const doc = document.documentElement
        doc.style.setProperty('--app-height', `${window.innerHeight}px`)
    }
    window.addEventListener('resize', appHeight)
    appHeight()

    import {me} from "./stores.js";
    import Header from "./lib/Header.svelte";

    let meValue;
    me.subscribe(v => meValue = v)

</script>

<div class="w-full h-full bg-slate-800 flex flex-col items-center p-3 gap-2 box-border overflow-hidden">
    <Header/>
    {#if !meValue}
        <Login/>
    {:else }
        <Chat/>
    {/if}
</div>
