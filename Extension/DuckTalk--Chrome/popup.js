
document.getElementById('btn').addEventListener('click', () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs.length === 0) return;
    const tabId = tabs[0].id;

    chrome.storage.local.get("divActivoTabId", (data) => {
      const actualTabActivo = data.divActivoTabId;

      if (actualTabActivo === tabId) {
        // Desactivar si ya está activo en esta pestaña
        chrome.storage.local.remove("divActivoTabId", () => {
          chrome.tabs.sendMessage(tabId, { action: "eliminar_div" });
          console.log('hola')
        });
      } else if (actualTabActivo == null) {
        // Activar si no está activo en ninguna pestaña
        chrome.storage.local.set({ divActivoTabId: tabId }, () => {
          chrome.tabs.sendMessage(tabId, { action: "crear_div" });
          console.log('chau')
        });
      } else {
        // Ya está activo en otra pestaña
      if (actualTabActivo) {
  chrome.tabs.get(actualTabActivo, (tab) => {
    if (chrome.runtime.lastError || !tab) {
      // La pestaña ya no existe -> limpiar estado y continuar
      chrome.storage.local.remove("divActivoTabId", () => {
        chrome.storage.local.set({ divActivoTabId: tabId }, () => {
          chrome.tabs.sendMessage(tabId, { action: "crear_div" });
        });
      });
    } else {
      // Todavía existe, mostrar error
      alert("❌ Ya hay una pestaña con el div activo. Cerrala antes de abrirlo en otra.");
    }
  });
}

      }
    });
  });
});

