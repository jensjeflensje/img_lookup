<template>
  <div v-if="!flashing"  @click="fileInput.click()">
    <div
    :class="{'dropzone': true, 'dropzone-active': active, 'dropzone-error': dropErrorText !== ''}"
    @dragenter.prevent="dragEnter"
    @dragleave.prevent="dragLeave"
    @dragover.prevent
    @drop.prevent="dropHandler">
    <div v-if="active" class="drop-hint">
      <span v-if="dropErrorText !== ''">{{ dropErrorText }}</span>
      <span v-else>Almost there...</span>
    </div>
  </div>
  <div v-if="!active" id="cursor-hint" ref="cursorHint" @click="fileInput.click()">
    <div
      class="hint-text"
      :style="hintTextStyle">
      {{ currentHint }}
    </div>
  </div>
  </div>
  <input
    ref="fileInput"
    type="file"
    :accept="acceptableFiles.join(',')"
    hidden
    @change="fileInputHandler">
  <div :class="{flashzone: true, 'flashzone-active': flashing}" ></div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, reactive, ref } from 'vue';

const emit = defineEmits(['file-chosen', 'animation-done']);

defineExpose({
  showError,
});

const hintTexts = [
  "Drop it like it's hot",
  "Come on, give it to me",
  "Gimme gimme",
  "Drop it right here",
  "Caught in 4K"
]

const acceptableFiles = [
  ".jpg",
  ".jpeg",
  ".png"
]

let lastCursorEvent: PointerEvent;
let active = ref(false);
let flashing = ref(false);
let currentHint = ref('Click or drag to select an image');
const hintTextStyle = reactive({transform: 'translate(-90px, -60px)'});
let hintInterval: number;
const cursorHint = ref();
const fileInput = ref();
const dropErrorText = ref('');


document.body.addEventListener('pointermove', (event) => lastCursorEvent = event)

function cursorHintMove() {
  if (active.value || flashing.value) return;
  if (lastCursorEvent) {
    cursorHint.value.style.left = (lastCursorEvent.pageX - 25) + 'px';
    cursorHint.value.style.top = (lastCursorEvent.pageY - 25) + 'px';
  }
  requestAnimationFrame(cursorHintMove);
}

function dragEnter() {
  active.value = true;
}

function dragLeave() {
  active.value = false;
  nextTick(cursorHintMove);
}

function showError(message: string) {
  dropErrorText.value = message;
  active.value = true;
  flashing.value = false;
  setTimeout(() => {
      dropErrorText.value = '';
      dragLeave();
    }, 2000);
}

function validateFileType(file: File) {
  if (!acceptableFiles.find(ext => file!.name.toLowerCase().endsWith(ext))) {
    dropErrorText.value = "Invalid file type"
    active.value = true;
    setTimeout(() => {
      dropErrorText.value = "";
      dragLeave();
    }, 1000);
    return false;
  }
  return true;
}

function chooseFile(file: File) {
  active.value = false;
  console.log(file);
  flashing.value = true;
  emit('file-chosen', file);
  setTimeout(() => {
    emit('animation-done', file);
  }, 500);
}

function fileInputHandler(event: Event) {
  const fileInputElement = event.target as HTMLInputElement;
  const file = fileInputElement.files![0];
  if (!validateFileType(file)) return;
  chooseFile(file);
}

function dropHandler(event: DragEvent) {
  let resultFile: File;
  // https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop#process_the_drop
  if (event.dataTransfer!.items) {
    // Use DataTransferItemList interface to access the file(s)
    [...event.dataTransfer!.items].forEach((item, _) => {
      // If dropped items aren't files, reject them
      if (item.kind === "file") {
        const file = item.getAsFile();
        if (file !== null) resultFile = file;
        return;
      }
    });
  } else {
    // Use DataTransfer interface to access the file(s)
    [...event.dataTransfer!.files].forEach((file, _) => {
      resultFile = file;
      return;
    });
  }
  if (!validateFileType(resultFile!)) return;

  chooseFile(resultFile!);
}

onMounted(() => {
  cursorHintMove();
  hintInterval = window.setInterval(
    () => {
      currentHint.value = hintTexts[Math.floor(Math.random() * hintTexts.length)]
      const direction = Math.random() > 0.5 ? 1 : -1;
      const translateX = (Math.random() * 40 + 40) * direction;
      const translateY = (Math.random() * 40 + 40) * direction;
      const rotate = (Math.random() * 60 - 30) * direction;
      hintTextStyle.transform = `translate(${translateX}px, ${translateY}px) rotate(${rotate}deg)`;
    },
    5000,
  )
})

onUnmounted(() => {
  clearInterval(hintInterval);
})
</script>

<style scoped>
  .dropzone {
    position: absolute;
    width: 100%;
    height: 100%;
    transition: all 300ms;
  }

  .dropzone-active {
    background-color: var(--primary-600);
  }

  .dropzone-error {
    background-color: var(--red-400);
  }

  @keyframes cursor-bubble {
    0% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.1);
    }
    100% {
      transform: scale(1);
    }
  }

  #cursor-hint {
    position: fixed;
    top: 35vh;
    left: 45vw;
    
    transform: translate(-50%,-50%);
    height: 50px;
    width: 50px;
    background-color: var(--primary-600);
    transition: all 100ms;
    border-radius: 50%;

    outline: 8px solid var(--primary-400);

    animation-name: cursor-bubble;
    animation-duration: 1500ms;
    animation-iteration-count: infinite;
    animation-timing-function: ease-in-out;

    cursor: pointer;
  }

  .hint-text {
    width: 250px;
    color: #2cb3824a;
    transition: all 100ms;
  }

  .drop-hint {
    display: flex;
    pointer-events: none;
    align-items: center;
    justify-content: center;
    font-size: 48px;
    height: 100%;
    animation: 200ms fade-in ease-in;
    color: var(--text-color)
  }

  .drop-hint > span {
    vertical-align: middle;
  }

  .flashzone {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    transition: all 300ms;
    display: none;
  }
  
  @keyframes flashzone-flash {
    0% {
      background-color: #00000000;
    }
    10% {
      background-color: #ffffffff;
    }
    100% {
      background-color: #00000000;
    }
  }

  .flashzone-active {
    animation: flashzone-flash 500ms;
    display: block;
  }
</style>
