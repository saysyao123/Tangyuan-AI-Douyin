import fs from 'node:fs';

const mainPath = process.argv[2];
if (!mainPath) throw new Error('usage: node inject_xiaochai_bridge.mjs <main.js>');

let source = fs.readFileSync(mainPath, 'utf8');
const importMarker = "  } = require('./dola-native-protocol');";
if (!source.includes("require('./xiaochai-bridge')")) {
  const index = source.indexOf(importMarker);
  if (index < 0) throw new Error('dola-native-protocol import marker not found');
  const end = index + importMarker.length;
  source = source.slice(0, end) + "\n  const { createXiaochaiBridge } = require('./xiaochai-bridge');" + source.slice(end);
}

const initMarker = '      if (accounts.length > 0) switchToAccount(accounts[0].id);';
const injected = [
  "      if (process.env.XIAOCHAI_DOLA_BRIDGE_ENABLED !== '0' && !global.__xiaochaiDolaBridge) {",
  '        try {',
  '          global.__xiaochaiDolaBridge = createXiaochaiBridge({',
  "            getAccounts: () => accounts.filter(a => a && a.site === 'dola').map((a, index) => ({",
  '              id: a.id,',
  '              name: a.name,',
  "              profileName: a.profileName || '',",
  "              authStatus: a.authStatus || 'unknown',",
  "              site: 'dola',",
  '              index',
  '            })),',
  "            findAccount: hostId => accounts.find(a => a && a.site === 'dola' && String(a.id) === String(hostId)) || null,",
  '            verifyAccount: async account => verifyDolaAccountSession(account),',
  '            activateAccount: async account => { switchToAccount(account.id); return true; },',
  '            getChainCache: account => {',
  '              const contents = dolaWebContentsByAccountId.get(account.id);',
  '              return contents && Array.isArray(contents.__xiaochaiDolaChainCache)',
  '                ? contents.__xiaochaiDolaChainCache.slice()',
  '                : [];',
  '            },',
  '            downloadForAccount: async (account, input) => {',
  '              const ses = session.fromPartition(account.partition);',
  "              const outputDir = process.env.XIAOCHAI_DOLA_BRIDGE_OUTPUT_DIR || path.join(getDownloadDir(), 'dola-bridge');",
  '              fs.mkdirSync(outputDir, { recursive: true });',
  "              const fileName = safeName(input.filename || 'dola-video.mp4', 'dola-video.mp4');",
  "              const destination = path.join(outputDir, String(Date.now()) + '_' + fileName);",
  '              const cookies = await collectCookiesForUrl({ session: ses }, input.url, account.partition);',
  '              const downloaded = await downloadUrlToFile(input.url, destination, cookies, {',
  "                referer: 'https://www.dola.com/',",
  '                requestSession: ses',
  '              });',
  "              if (!downloaded || downloaded.success !== true) throw Object.assign(new Error('host download failed'), { code: 'DOWNLOAD_FAILED' });",
  '              const valid = validateDownloadedMediaFile(destination);',
  "              if (!valid.success) throw Object.assign(new Error('invalid media'), { code: 'INVALID_MEDIA' });",
  '              return { path: destination, bytes: Number(downloaded.bytes) || 0 };',
  '            },',
  '            appVersion: () => APP_VERSION',
  '          });',
  '          global.__xiaochaiDolaBridge.start();',
  '        } catch (error) {',
  "          console.error('[Xiaochai] local bridge failed to start:', error && error.code ? error.code : 'BRIDGE_START_FAILED');",
  '        }',
  '      }',
  ''
].join('\n');
if (!source.includes('global.__xiaochaiDolaBridge')) {
  const index = source.indexOf(initMarker);
  if (index < 0) throw new Error('initializeMainApp marker not found');
  const newline = source.indexOf('\n', index + initMarker.length);
  const end = newline < 0 ? source.length : newline + 1;
  source = source.slice(0, end) + injected + source.slice(end);
}

fs.writeFileSync(mainPath, source, 'utf8');
console.log(`injected Xiaochai bridge into ${mainPath}`);
