<template>
  <button class="create-game-button" @click="createGame">
    Create new game!!!
  </button>
  <form class="create-game-form" v-if="isGameCreated">
    <input
      v-model="playerName"
      type="text"
      name="player.name"
      class="player-name"
    />
    <input
      v-model="secsPerRound"
      type="text"
      name="game.secs-per-round"
      class="secs-per-round"
    />
    <button @click="initiateGame" class="start-game-button">
      INITIATE GAME!!! LOL
    </button>
  </form>
  <div v-if="isGameStarted">
    {{ backEndPayload }}
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { GameManager } from '../services/GameManager';

export default defineComponent({
  name: 'HelloWorld',
  setup() {
    const isGameCreated = ref(false);
    const isGameStarted = ref(false);
    const backEndPayload = ref({});

    const playerName = ref('John Connor');
    const secsPerRound = ref('90');
    const createGame = () => {
      isGameCreated.value = true;
    };
    const initiateGame = async () => {
      backEndPayload.value = await GameManager.requestGameData(
        playerName.value,
        secsPerRound.value
      );
    };
    return {
      createGame,
      initiateGame,
      isGameCreated,
      playerName,
      secsPerRound,
      isGameStarted,
      backEndPayload,
    };
  },
});
</script>

<style lang="scss" scoped></style>
