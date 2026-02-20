<script setup>
import { ref, computed, onUnmounted } from "vue";

import { arrWorlds, arrBlockedWorlds, arrAction } from "./constants"

const URL_API = `${import.meta.env.VITE_API}`;

// Практическая работа №1

const dataTransmission = ref(false);
const intervalMany = ref(null);
const intervalOne = ref(null);

const nameStatus = computed(() =>
  dataTransmission.value
    ? "Сообщения отправляются"
    : "Сообщения не отправляютя",
);
const nameButtonTransmission = computed(() =>
  dataTransmission.value
    ? "Остановить передачу сообщений"
    : "Включить передачу сообщений",
);

function setStatusTransmission() {
  dataTransmission.value = !dataTransmission.value;
  if (dataTransmission.value) {
    intervalMany.value = setInterval(() => {
      sendOneMessage("many");
    }, 1000);
    intervalOne.value = setInterval(() => {
      sendOneMessage("one");
    }, 10000);
    sendOneMessage("many");
    sendOneMessage("one");
  } else {
    if (intervalMany.value) {
      clearInterval(intervalMany.value);
      intervalMany.value = null;
    }
    if (intervalOne.value) {
      clearInterval(intervalOne.value);
      intervalOne.value = null;
    }
  }
}

function sendOneMessage(keyMessage) {
  const textMsg =
    keyMessage === "one" ? "Одиночное сообщение" : "Пакетное сообщение";
  const isoDate =  new Date().toISOString();
  try {
    fetch(`${URL_API}/message`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ key: keyMessage, msg: `${isoDate}: ${textMsg}` }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json().then((res) => {
            console.log("Cooбщение отправлено!");
            console.log(res.msg);
          });
        } else {
          console.error("Ошибка отправки сообщения: ", response.status);
        }
      })
      .catch((err) => {
        console.error("Ошибка сети: ", err);
      });
  } catch (error) {
    console.error("Ошибка в sendOneMessage(): ", error);
  }
}

// Практическая работа №2

const dataTestTransmission = ref(false);
const intervalTestMassage = ref(null);
const testMessageCount = ref(0);
const blockedMessageCount = ref(0);

const nameTestStatus = computed(() =>
  dataTestTransmission.value
    ? "Тестовые сообщения отправляются"
    : "Тестовые сообщения не отправляютя",
);
const nameButtonTestTransmission = computed(() =>
  dataTestTransmission.value
    ? "Остановить тестовую переписку"
    : "Включить тестовую переписку",
);

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function sendTestMessage() {
  // Увеличиваем счетчик сообщений
  testMessageCount.value++;

  // Генерация user_id и recipient_id (разные числа от 1 до 21)
  let user_id, recipient_id;
  do {
    user_id = getRandomInt(1, 21).toString();
    recipient_id = getRandomInt(1, 21).toString();
  } while (user_id === recipient_id);

  // Текущее время в формате строки
  const timestamp = new Date().toISOString();

  // Выбор трех случайных слов из arrWorlds
  const words = [];
  for (let i = 0; i < 3; i++) {
    const randomIndex = Math.floor(Math.random() * arrWorlds.length);
    words.push(arrWorlds[randomIndex]);
  }

  // Формирование сообщения
  let message = words.join(" ");

  // Каждое третье сообщение добавляем слово из arrBlockedWorlds
  if (testMessageCount.value % 3 === 0) {
    const blockedWordIndex = Math.floor(Math.random() * arrBlockedWorlds.length);
    const blockedWord = arrBlockedWorlds[blockedWordIndex];
    message += " " + blockedWord;
  }

  // Отправка POST-запроса
  try {
    fetch(`${URL_API}/user-message`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        user_id,
        recipient_id,
        timestamp,
        message,
      }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json().then((res) => {
            console.log("Тестовое сообщение отправлено!");
            console.log(res.msg);
          });
        } else {
          console.error(
            "Ошибка отправки тестового сообщения: ",
            response.status
          );
        }
      })
      .catch((err) => {
        console.error("Ошибка сети при отправке тестового сообщения: ", err);
      });
  } catch (error) {
    console.error("Ошибка в sendTestMessage(): ", error);
  }
}

function sendStatusBlocked() {
  // Увеличиваем счетчик сообщений
  blockedMessageCount.value++;

  // Генерация user_id и blocked_user_id (разные числа от 1 до 21)
  let user_id, blocked_user_id;
   if (blockedMessageCount.value % 3 === 0) {
    const blockedWordIndex = Math.floor(Math.random() * arrBlockedWorlds.length);
    const blockedWord = arrBlockedWorlds[blockedWordIndex];
    user_id = 'forbidden_words'
    blocked_user_id = blockedWord
  } else {
    do {
      user_id = getRandomInt(1, 21).toString();
      blocked_user_id = getRandomInt(1, 21).toString();
    } while (user_id === blocked_user_id);
  }

  // Текущее время в формате строки
  const timestamp = new Date().toISOString();

  // Назначаем действие
  const action = blockedMessageCount.value % 2 === 0 ? 'unblocked' : 'blocked';

  // Отправка POST-запроса
  try {
    fetch(`${URL_API}/blocked-message`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        user_id,
        blocked_user_id,
        timestamp,
        action
      }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json().then((res) => {
            console.log("Cообщение о блокировке/разблокировке отправлено!");
            console.log(res.msg);
          });
        } else {
          console.error(
            "Ошибка отправки сообщения о блокировке/разблокировке: ",
            response.status
          );
        }
      })
      .catch((err) => {
        console.error("Ошибка сети при отправке сообщения о блокировке/разблокировке: ", err);
      });
  } catch (error) {
    console.error("Ошибка в sendStatusBlocked(): ", error);
  }
}

function setStatusTestTransmission() {
  dataTestTransmission.value = !dataTestTransmission.value;
  if (dataTestTransmission.value) {
    // Запускаем отправку каждую секунду
    intervalTestMassage.value = setInterval(() => {
      sendTestMessage();
      sendStatusBlocked();
    }, 1000);
    // Сразу отправляем первое сообщение
    sendTestMessage();
    sendStatusBlocked();
  } else {
    // Останавливаем отправку
    if (intervalTestMassage.value) {
      clearInterval(intervalTestMassage.value);
      intervalTestMassage.value = null;
    }
  }
}

onUnmounted(() => {
  if (intervalMany.value) clearInterval(intervalMany.value);
  if (intervalOne.value) clearInterval(intervalOne.value);
  if (intervalTestMassage.value) clearInterval(intervalTestMassage.value);
});
</script>

<template>
  <div>
    <div>
      <p>Практическая работа №1</p>
      <p>
        Состояние отправки сообщений:
        <span
          :class="{
            'status-transmission-active': dataTransmission === true,
            'status-transmission-unactive': dataTransmission === false,
          }"
        >
          {{ nameStatus }}
        </span>
      </p>
      <button @click="setStatusTransmission">
        {{ nameButtonTransmission }}
      </button>
    </div>
    <div>
      <p>Практическая работа №2</p>
      <p>
        Состояние отправки тестовых сообщений:
        <span
          :class="{
            'status-test-transmission-active': dataTestTransmission === true,
            'status-test-transmission-unactive': dataTestTransmission === false,
          }"
        >
          {{ nameTestStatus }}
        </span>
      </p>
      <button @click="setStatusTestTransmission">
        {{ nameButtonTestTransmission }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.status-test-transmission-active,
.status-transmission-active {
  color: green;
}

.status-test-transmission-unactive,
.status-transmission-unactive {
  color: red;
}

button {
  margin-top: 10px;
  padding: 8px 16px;
  cursor: pointer;
}
</style>
