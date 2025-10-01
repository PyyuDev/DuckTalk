let botonIniciar,
  botondetener,
  player,
  deleteimagecat = false;

function insertarDiv() {
  if (document.getElementById("mi-div-flotante")) return;

  const div = document.createElement("div");
  div.id = "mi-div-flotante";
  Object.assign(div.style, {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    color: "white",
    padding: "10px",
    zIndex: 100000,
    borderRadius: "5px",
    fontFamily: "Arial",
    width: "300px",
    height: "370px",
    overflow: "auto",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "column",
  });

  div.innerHTML = `
    <audio id="player"></audio>
    <img id="image" alt="er" width="200" height="200" />
 <div class="div_botones">
    <button id="iniciar" class="boton_iniciar" >Iniciar</button>
    <button id="detener" class="boton_iniciar" disabled>Detener</button>
    </div>
  `;

  // Botón de cerrar (❌)
  /*  const btnCerrar = document.createElement("button");
  btnCerrar.textContent = "✖";
  Object.assign(btnCerrar.style, {
    position: "absolute",
    top: "2px",
    right: "5px",
    background: "transparent",
    color: "white",
    border: "none",
    fontSize: "16px",
    cursor: "pointer",
  });
  btnCerrar.onclick = () => {
    div.remove();

    chrome.runtime.sendMessage({ action: "eliminar_div" });

    chrome.runtime.sendMessage({ action: "cerrar_div_manual" }); // Extra si querés avisar al background
  };

  div.appendChild(btnCerrar); */
  document.body.appendChild(div);

  function cargarImagen(nombreArchivo) {
    imagen.src = chrome.runtime.getURL(nombreArchivo);
  }

  // Variables
  const estado = div.querySelector("#estado");
  player = div.querySelector("#player");
  botonIniciar = div.querySelector("#iniciar");
  botondetener = div.querySelector("#detener");
  const imagen = div.querySelector("#image");
  cargarImagen("duck.png");

  let stream = null;
  let audioContext = null;
  let source = null;
  let analyser = null;
  let dataArray = null;
  let mediaRecorder = null;
  let conversacionActiva = false;
  deleteimagecat = false;
  let seDetectoAudio = false;

  const umbralSilencio = 10;
  const maxSilencio = 3000;
  let ultimoSonido = Date.now();
  let grabando = false;

  // 🎙️ Iniciar grabación

  async function iniciarConversacion() {
    conversacionActiva = true;
    seDetectoAudio = false;

    try {
      // ✅ 1. Verificar acceso al micrófono
      await navigator.mediaDevices.getUserMedia({ audio: true });
      botonIniciar.disabled = true;
      botondetener.disabled = false;
      // ✅ 2. Si el permiso fue otorgado, podemos avanzar
      if (!deleteimagecat) {
        cargarImagen("cat.gif");
      }

      const response = await fetch("http://127.0.0.1:8000/iniciar");

      if (!response.ok) {
        throw new Error("Error en /iniciar");
      }

      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);

      player.src = audioUrl;
      if (!deleteimagecat) {
        cargarImagen("talk.gif");
        await player.play();
      }

      player.onended = () => {
        if (!deleteimagecat) {
          empezarGrabacion();
        }
      };
    } catch (err) {
      console.error(
        "❌ No se pudo iniciar conversación o activar el micrófono:",
        err
      );
     /*  estado.textContent = "❌ Necesitás permitir el uso del micrófono."; */
      showToast("Necesitás permitir el uso del micrófono. Cuack!")
      conversacionActiva = false;
    }
  }

  async function empezarGrabacion() {
    if (!conversacionActiva) return;
    /* estado.textContent = "⏺️ Grabando... habla ahora"; */

    if (!stream) {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    }

    if (!audioContext) {
      audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }

    if (source) source.disconnect();
    source = audioContext.createMediaStreamSource(stream);

    analyser = audioContext.createAnalyser();
    analyser.fftSize = 512;
    source.connect(analyser);
    dataArray = new Uint8Array(analyser.frequencyBinCount);

    const chunks = [];
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
    cargarImagen("listen.png");

    mediaRecorder.onstop = async () => {
      grabando = false;
     /*  estado.textContent = "📤 Enviando audio al backend..."; */
      const blob = new Blob(chunks, { type: "audio/webm" });

      if (!deleteimagecat) {
        cargarImagen("cat.gif");
      }
      if (seDetectoAudio) {
        try {
          const formData = new FormData();
          formData.append("audio", blob, "grabacion.webm");

          const response = await fetch("http://localhost:8000/conversar", {
            method: "POST",
            body: formData,
          });

          if (!response.ok) throw new Error("Error en el servidor");

          const contentType = response.headers.get("content-type") || "";
          if (contentType.includes("audio/wav") && !deleteimagecat) {
            cargarImagen("talk.gif");
          }

          const patoBlob = await response.blob();
          const patoUrl = URL.createObjectURL(patoBlob);

          player.src = patoUrl;
          if (!deleteimagecat) {
            await player.play();
          }

         /*  estado.textContent = "🦆 El patito respondió. Escuchando..."; */

          player.onended = () => {
            if (!deleteimagecat) {
              empezarGrabacion();
            }
          };
        } catch (err) {
          console.error("❌ Error al enviar o recibir audio:", err);
          /* estado.textContent = "❌ Error al comunicar con el servidor."; */
        } finally {
          seDetectoAudio = false;
        }
      } else {
        detenerConversacion();

        showToast("Si no hablas en 3 segundo,tienes que volver a empezar la conversacion! cuack!");
      }
    };

    grabando = true;
    mediaRecorder.start();
    ultimoSonido = Date.now();

    function detectarSilencio() {
      analyser.getByteFrequencyData(dataArray);
      const volumen = dataArray.reduce((a, b) => a + b, 0) / dataArray.length;

      if (volumen > umbralSilencio) {
        ultimoSonido = Date.now();
        seDetectoAudio = true;
      }

      if (volumen < umbralSilencio) {
        if (Date.now() - ultimoSonido > maxSilencio && grabando) {
          /* estado.textContent = "🛑 Silencio detectado, deteniendo grabación..."; */
          mediaRecorder.stop();
          return;
        }
      } else {
        ultimoSonido = Date.now();
      }

      if (grabando) {
        requestAnimationFrame(detectarSilencio);
      }
    }

    detectarSilencio();
  }

  // 🚀 Iniciar conversación

  // 🛑 Detener conversación
  async function detenerConversacion() {
    deleteimagecat = true;
    player.pause();
    player.currentTime = 0;
    botonIniciar.disabled = false;
    /*  chrome.storage.local.set({ estadoGlobal: "inactivo" }); */
    botondetener.disabled = true;
    chrome.storage.local.remove("divActivoTabId", () => {});
    conversacionActiva = false;
    cargarImagen("duck.png");
    await new Promise((r) => setTimeout(r, 100));
   /*  estado.textContent = "🛑 Conversación detenida."; */

    try {
      await fetch("http://127.0.0.1:8000/cerrar");
      botonIniciar.disabled = false;
    } catch (e) {
      console.error("Error cerrando backend:", e);
    }

    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
    }

    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      stream = null;
    }

    if (audioContext) {
      audioContext.close();
      audioContext = null;
    }
  }

  // 🎛️ Eventos botones
  botonIniciar.onclick = () => {
    deleteimagecat = false;
    iniciarConversacion();
  };

  botondetener.onclick = () => {
    detenerConversacion();
  };

  chrome.runtime.onMessage.addListener((request) => {
    if (request.action === "forzar_detener_conversacion") {
      deleteimagecat = true;
      player.pause();
      player.currentTime = 0;
      botonIniciar.disabled = false;
      botondetener.disabled = true;
      chrome.runtime.sendMessage({ action: "cerrar_div_manual" });
      chrome.runtime.sendMessage({ action: "eliminar_div" });
      detenerConversacion();
    }
  });
function showToast(message = "Algo salió mal") {
  // Evita duplicados
  if (document.getElementById("toast-extension")) return;

  // Crear contenedor principal
  const toast = document.createElement("div");
  toast.id = "toast-extension";

  // Estilos modernos tipo react-hot-toast con flex
  toast.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #9300e6;
    color: #fff;
    padding: 12px 16px;
    border-radius: 8px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.2);
    font-family: system-ui, sans-serif;
    font-size: 14px;
    z-index: 999999;
    display: flex;
    align-items: center;
    gap: 10px;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.3s ease, transform 0.3s ease;
  `;

  // Crear imagen (opcional)

    const imgduck = document.createElement("img");
    imgduck.src = chrome.runtime.getURL("icon.png");
    imgduck.alt = "icono";
    imgduck.style.cssText = `
      width: 20px;
      height: 20px;
    `;
    toast.appendChild(imgduck);


  // Crear párrafo de texto
  const text = document.createElement("p");
  text.textContent = message;
  text.style.margin = 0;
  text.style.color= "white"

  toast.appendChild(text);

  document.body.appendChild(toast);

  // Activar animación
  requestAnimationFrame(() => {
    toast.style.opacity = "1";
    toast.style.transform = "translateY(0)";
  });

  // Eliminar después de 3 segundos
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(20px)";
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, 3000);
}

}

// ❌ Eliminar div
function eliminarDiv() {
  const div = document.getElementById("mi-div-flotante");
  if (div) div.remove();
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "crear_div") {
    insertarDiv();
  } else if (request.action === "eliminar_div") {
    eliminarDiv();
  } else if (request.action === "forzar_detener_conversacion") {
    deleteimagecat = true;
    if (player) {
      player.pause();
      player.currentTime = 0;
    }
    if (botonIniciar) botonIniciar.disabled = false;
    if (botondetener) botondetener.disabled = true;

    chrome.runtime.sendMessage({ action: "cerrar_div_manual" });
    chrome.runtime.sendMessage({ action: "eliminar_div" });

    detenerConversacion();
  }
});

// Mostrar div si esta pestaña está marcada como activa
chrome.runtime.sendMessage({ action: "check_tab" }, (response) => {
  if (response?.divActivo) {
    insertarDiv();
  }
});
