chrome.runtime.onInstalled.addListener(() => {
  console.log("Extensión instalada.");
});

// Responde al content script si el div debe estar visible
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "check_tab" && sender.tab) {
    const tabId = sender.tab.id;

    chrome.storage.local.get("divActivoTabId", (data) => {
      const divActivo = data.divActivoTabId === tabId;
      sendResponse({ divActivo });
    });

    return true; // Necesario para enviar respuesta asincrónica
  }
});

// Limpia estado si se cierra la pestaña activa
chrome.tabs.onRemoved.addListener((closedTabId, removeInfo) => {
  chrome.storage.local.get("divActivoTabId", (data) => {
    const activoId = data.divActivoTabId;
    if (activoId && parseInt(activoId) === closedTabId) {
      console.log(`🧹 Limpiando estado porque se cerró la pestaña activa: ${closedTabId}`);
      chrome.storage.local.remove("divActivoTabId");
    }
  });
});



chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "cerrar_div_manual" && sender.tab?.id != null) {
    chrome.storage.local.get("divActivoTabId", (data) => {
      if (data.divActivoTabId === sender.tab.id) {
        chrome.storage.local.remove("divActivoTabId", () => {
          console.log("✅ divActivoTabId eliminado manualmente desde content.js");
        });
      }
    });
  }
});




