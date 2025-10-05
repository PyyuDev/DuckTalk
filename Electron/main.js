const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
function createWindow() {
  const win = new BrowserWindow({
    width: 300,
    height: 300,
    resizable: false,
    alwaysOnTop: true,
    transparent: true,
    frame: false,
    icon: path.join(__dirname, 'assets', 'icon.png'),
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,  // para poder usar require en renderer (no recomendado, pero lo tienes así)
    },
  });

  win.loadFile("index.html");
  win.removeMenu();
/*   win.webContents.openDevTools(); */


  // Listeners para IPC
  ipcMain.on("minimize-window", () => {
    win.minimize();
  });

  ipcMain.on("close-window", () => {
    win.close();
  });
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
