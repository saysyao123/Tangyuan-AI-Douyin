'use strict';

const { dialog, ipcMain } = require('electron');

let registered = false;

function registerPortableDialogIpc() {
  if (registered) return;
  registered = true;

  ipcMain.handle('portable:pick-image', async (event) => {
    const owner = event.sender?.getOwnerBrowserWindow?.() || undefined;
    const result = await dialog.showOpenDialog(owner, {
      title: '选择 Seedance 首帧图片',
      properties: ['openFile'],
      filters: [
        { name: '图片', extensions: ['png', 'jpg', 'jpeg', 'webp'] },
        { name: '所有文件', extensions: ['*'] }
      ]
    });
    if (result.canceled || !Array.isArray(result.filePaths) || !result.filePaths[0]) return null;
    return String(result.filePaths[0]);
  });
}

module.exports = { registerPortableDialogIpc };
