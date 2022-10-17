const {app, BrowserWindow} = require('electron')
const isDev = require("electron-is-dev")
const path = require("path")
const {PythonShell} = require("python-shell");
require('@electron/remote/main').initialize()

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            enableRemoteModule: true
        }
    })
    win.webContents.openDevTools();
    win.removeMenu();
    win.loadURL(
        isDev ? 'http://localhost:3000' : `file://${path.join(__dirname, '/build/index.html')}`
    );

    const py_path = path.join(__dirname, '');
    const python_exe_path = path.join(__dirname, '../backend/venv/Scripts/python.exe');
    const py_shell_options = {
        mode: 'text',
        pythonPath: python_exe_path,
        pythonOptions: ['-u'],
        scriptPath: py_path
    };
    let pyshell = new PythonShell('../backend/main.py', py_shell_options);
    pyshell.on('message', function (message) {
        console.log(message);
    });
    pyshell.on('error', function (message) {
        console.log(message);
    });
}

app.on("ready", createWindow)

app.on("window-all-closed", function () {
    app.quit();
})

app.on("activate", function () {
    createWindow()
})