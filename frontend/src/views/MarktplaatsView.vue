<template>
  <div class="container">
    <div class="lookup-box">
      <h2>Look up a listing</h2>
      <InputText class="input-field" v-model="inputLink" placeholder="https://marktplaats.nl/..." />
      <br/>
      <br/>
      <Button size="small" @click="fetchAd()" label="Submit" />
      <div v-if="output !== undefined" class="output-box">
        <strong>Listing</strong>: {{ output.name }}
        <br/>
        <strong>Seller</strong>: {{ output.author }}
        <br/>
        <strong>Latitude</strong>: {{ output.latitude }}
        <br/>
        <strong>Longitude</strong>: {{ output.longitude }}
        <br/>
        <strong>Zip code</strong>: {{ output.zipCode }}
      </div>
    </div>
  </div>


</template>

<script setup lang="ts">
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import {ref} from "vue";
import {fetchMarktplaatsInfo} from "@/api.ts";
import MarktplaatsResponse from "@/types/MarktplaatsResponse.ts";

const inputLink = ref('');
let output: MarktplaatsResponse | undefined = undefined;

async function fetchAd() {
  output = await fetchMarktplaatsInfo(inputLink.value);
  inputLink.value = '';
}

</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
}
.lookup-box {
  margin: 32px auto;
  max-width: 600px;
  width: 100%;
  padding: 0 16px;
}
.input-field {
  width: 360px;
  max-width: 100%;
}
.output-box {
  margin-top: 24px;
}
</style>
