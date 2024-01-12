<template>
  <div class="title-text">
    <h1>Oh no... this page doesn't exist.</h1>
    <h3>Could you help me fix it?</h3>
    <p>
      Maybe you could fix it by editing the CSS?
    </p>
    <component :is="'style'" contenteditable class="editor-box">
      .title-text {
        margin: 0 auto;
        max-width: 700px;
        padding: 22px;
        color: #ffffffde;
      }
    </component>
  </div>

</template>

<script setup lang="ts">


</script>

<style scoped>
  .editor-box {
    display: block;
    font-family: monospace;
  }
</style>
