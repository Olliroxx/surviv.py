//Json parsed
(window['webpackJsonp'] = window['webpackJsonp'] || [])['push']([
    [0], {
        '00000000': function(_0x1f0b71, _0x4c5f59, _0x314869) {
            'use strict';
            var _0x6feadf = [_0x314869('00000001'), _0x314869('00000002'), _0x314869('00000003'), _0x314869('00000004')],
                _0x2f5cfd = {};
            for (var _0x20fa2e = 0; _0x20fa2e < _0x6feadf['length']; _0x20fa2e++) {
                var _0x2e087f = _0x6feadf[_0x20fa2e],
                    _0x41d912 = Object['keys'](_0x2e087f);
                for (var _0x625e2a = 0; _0x625e2a < _0x41d912['length']; _0x625e2a++) {
                    var _0x56f5b7 = _0x41d912[_0x625e2a];
                    if (_0x2f5cfd[_0x56f5b7] !== undefined) throw new Error('GameObject\x20' + _0x56f5b7 + '\x20is\x20already\x20defined');
                    _0x2f5cfd[_0x56f5b7] = _0x2e087f[_0x56f5b7];
                }
            }
            _0x1f0b71['exports'] = _0x2f5cfd;
        },
        '00000001': function(_0x0000, _0x0000, _0x0000) {
            'use strict';
            var _0x563ec2 = _0x5466b4('00000000');

            function _0x50f1e7(_0x58022b, _0x2d6016) {
                return _0x563ec2['mergeDeep']({}, _0x4d149b[_0x58022b], {
                    'baseType': _0x58022b
                }, _0x2d6016);
            }
            var _0x4d149b = {
                'bullet_template': {
                        'type': 'bullet',
                        'damage': 0x0,
                        'obstacleDamage': 0x0,
                        'falloff': 0.0,
                        'distance': 0x00,
                        'speed': 0x00,
                        'variance': 0x0,
                        'shrapnel': false,
                        'tracerColor': '9mm',
                        'tracerWidth': 0.0,
                        'tracerLength': 0.0
                },
                'bullet_fakegun1': {
                    'type': 'bullet',
                    'damage': 0x0,
                    'obstacleDamage': 0x1,
                    'falloff': 0.0,
                    'distance': 0x00 + 0,
                    'speed': 0x00 + 1,
                    'variance': (0x0 + 1) * 7.5 / (3 + 2),
                    'shrapnel': false,
                    'tracerColor': 'test\x20tracer\x20color',
                    'tracerWidth': Math['PI'],
                    'tracerLength': 0.0
                },
                'bullet_fakegun2': {
                    'type': 'bullet',
                    'damage': 0x0,
                    'obstacleDamage': 0x0,
                    'falloff': 0.0,
                    'distance': 0x00,
                    'speed': 0x00,
                    'variance': 0x0,
                    'shrapnel': false,
                    'tracerColor': 'tallow\x27s_tracerColor',
                    'tracerWidth': 0.0,
                    'tracerLength': 0.0
                },
                'falloff_filler': {
                    'falloff1': 'falloff',
                    'falloff2': 'falloff'
                }
            },
                _0x42949b = 1.25,
                _0x7c2636 = 1.5,
                _0x474629 = {
                    'bullet_template_bonus': _0x50f1e7('bullet_template', {
                        'speed': 85 * _0x42949b,
                        'distance': 100 * _0x7c2636
                    }),
                    'bullet_fakegun1_bonus': _0x50f1e7('bullet_fakegun1', {
                        'speed': 85 * _0x42949b,
                        'distance': 100 * _0x7c2636
                    }),
                    'bullet_fakegun2_bonus': _0x50f1e7('bullet_fakegun2', {
                        'speed': 85 * _0x42949b,
                        'distance': 100 * _0x7c2636
                    })
                },
                _0x4b9012 = _0x563ec2['mergeDeep']({}, _0x4d149b, _0x474629);
            _0x2327af['exports'] = _0x4b9012;
        },
        '00000002': function(_0x0000, _0x0000, _0x0000) {
            'use strict';
            var _0x563ec2 = _0x5466b4('00000000');

            var _0x306286 = {
                'explosion_template': {
                    'type': 'explosion',
                    'damage': 0x0,
                    'obstacleDamage': 0,
                    'rad': {
                        'min': 0,
                        'max': 0
                    },
                    'shrapnelCount': 0,
                    'shrapnelType': 'shrapnel_frag',
                    'explosionEffectType': 'frag',
                    'decalType': 'decal_frag_explosion'
                },
                'explosion_1': {
                    'type': 'explosion',
                    'damage': 0x1,
                    'obstacleDamage': 1,
                    'rad': {
                        'min': 3,
                        'max': 5
                    },
                    'shrapnelCount': 7,
                    'shrapnelType': 'shrapnel_frag',
                    'explosionEffectType': 'frag',
                    'decalType': 'decal_frag_explosion'
                },
                'explosionEffectType_filler': {
                    'explosionEffectType1': 'explosionEffectType',
                    'explosionEffectType2': 'explosionEffectType',
                    'explosionEffectType3': 'explosionEffectType',
                    'explosionEffectType4': 'explosionEffectType'
                }
            };
            _0x2327af['exports'] = _0x4b9012;
        },
        '00000003': function(_0x0000, _0x0000, _0x0000) {
            'use strict';
            var _0x563ec2 = _0x5466b4('00000000');

            var _0x3b8fcb = {
                    'Locked': 0x0,
                    'Faces': 0x1,
                    'Food': 0x2,
                    'Animals': 0x3,
                    'Logos': 0x4,
                    'Other': 0x5,
                    'Flags': 0x6,
                    'Default': 0x63
                },
                _0x109274 = {
                    'emote_template': {
                        'type': 'emote',
                        'texture': '',
                        'sound': 'emote_01',
                        'channel': 'ui',
                        'teamOnly': true,
                        'noCustom': true,
                        'category': _0x3b8fcb['Locked']
                    },
                    'emote_medical': {
                        'type': 'emote',
                        'texture': 'emote-medical-healthkit.img',
                        'sound': 'emote_01',
                        'channel': 'ui',
                        'teamOnly': true,
                        'noCustom': true,
                        'category': _0x3b8fcb['Locked']
                    },
                    'emote_ammo': {
                        'type': 'emote',
                        'texture': 'ammo-box.img',
                        'sound': 'emote_01',
                        'channel': 'ui',
                        'teamOnly': true,
                        'noCustom': true,
                        'category': _0x3b8fcb['Locked']
                    },
                    'emote_ammo9mm': {
                        'type': 'emote',
                        'texture': 'ammo-9mm.img',
                        'sound': 'emote_01',
                        'channel': 'ui',
                        'teamOnly': true,
                        'noCustom': true,
                        'category': _0x3b8fcb['Locked']
                    },
                    'emote_filler': {
                        'emote1': 'emote'
                        'emote2': 'emote'
                        'emote3': 'emote'
                        'emote4': 'emote'
                        'emote5': 'emote'
                        'emote6': 'emote'
                        'emote7': 'emote'
                        'emote8': 'emote'
                        'emote9': 'emote'
                        'emote10': 'emote'
                        'emote11': 'emote'
                        'emote12': 'emote'
                        'emote13': 'emote'
                        'emote14': 'emote'
                        'emote15': 'emote'
                        'emote16': 'emote'
                        'emote17': 'emote'
                        'emote18': 'emote'
                        'emote19': 'emote'
                        'emote20': 'emote'
                        'emote21': 'emote'
                        'emote22': 'emote'
                        'emote23': 'emote'
                        'emote24': 'emote'
                        'emote25': 'emote'
                        'emote26': 'emote'
                        'emote27': 'emote'
                        'emote28': 'emote'
                        'emote29': 'emote'
                        'emote30': 'emote'
                        'emote31': 'emote'
                        'emote32': 'emote'
                        'emote33': 'emote'
                        'emote34': 'emote'
                        'emote35': 'emote'
                        'emote36': 'emote'
                        'emote37': 'emote'
                        'emote38': 'emote'
                        'emote39': 'emote'
                        'emote40': 'emote'
                        'emote41': 'emote'
                        'emote42': 'emote'
                        'emote43': 'emote'
                        'emote44': 'emote'
                        'emote45': 'emote'
                        'emote46': 'emote'
                        'emote47': 'emote'
                        'emote48': 'emote'
                        'emote49': 'emote'
                        'emote50': 'emote'
                        'emote51': 'emote'
                        'emote52': 'emote'
                        'emote53': 'emote'
                        'emote54': 'emote'
                        'emote55': 'emote'
                        'emote56': 'emote'
                        'emote57': 'emote'
                        'emote58': 'emote'
                        'emote59': 'emote'
                        'emote60': 'emote'
                        'emote61': 'emote'
                        'emote62': 'emote'
                        'emote63': 'emote'
                        'emote64': 'emote'
                        'emote65': 'emote'
                        'emote66': 'emote'
                        'emote67': 'emote'
                        'emote68': 'emote'
                        'emote69': 'emote'
                        'emote70': 'emote'
                        'emote71': 'emote'
                        'emote72': 'emote'
                        'emote73': 'emote'
                        'emote74': 'emote'
                        'emote75': 'emote'
                        'emote76': 'emote'
                        'emote77': 'emote'
                        'emote78': 'emote'
                        'emote79': 'emote'
                        'emote80': 'emote'
                        'emote81': 'emote'
                        'emote82': 'emote'
                        'emote83': 'emote'
                        'emote84': 'emote'
                        'emote85': 'emote'
                        'emote86': 'emote'
                        'emote87': 'emote'
                        'emote88': 'emote'
                        'emote89': 'emote'
                        'emote90': 'emote'
                        'emote91': 'emote'
                        'emote92': 'emote'
                        'emote93': 'emote'
                        'emote94': 'emote'
                        'emote95': 'emote'
                        'emote96': 'emote'
                        'emote97': 'emote'
                        'emote98': 'emote'
                        'emote99': 'emote'
                        'emote100': 'emote'
                        'emote101': 'emote'
                        'emote102': 'emote'
                        'emote103': 'emote'
                        'emote104': 'emote'
                        'emote105': 'emote'
                        'emote106': 'emote'
                        'emote107': 'emote'
                        'emote108': 'emote'
                        'emote109': 'emote'
                        'emote110': 'emote'
                        'emote111': 'emote'
                        'emote112': 'emote'
                        'emote113': 'emote'
                        'emote114': 'emote'
                        'emote115': 'emote'
                        'emote116': 'emote'
                        'emote117': 'emote'
                        'emote118': 'emote'
                        'emote119': 'emote'
                        'emote120': 'emote'
                        'emote121': 'emote'
                        'emote122': 'emote'
                        'emote123': 'emote'
                        'emote124': 'emote'
                        'emote125': 'emote'
                        'emote126': 'emote'
                        'emote127': 'emote'
                        'emote128': 'emote'
                        'emote129': 'emote'
                        'emote130': 'emote'
                        'emote131': 'emote'
                        'emote132': 'emote'
                        'emote133': 'emote'
                        'emote134': 'emote'
                        'emote135': 'emote'
                        'emote136': 'emote'
                        'emote137': 'emote'
                        'emote138': 'emote'
                        'emote139': 'emote'
                        'emote140': 'emote'
                        'emote141': 'emote'
                        'emote142': 'emote'
                        'emote143': 'emote'
                        'emote144': 'emote'
                        'emote145': 'emote'
                        'emote146': 'emote'
                        'emote147': 'emote'
                        'emote148': 'emote'
                        'emote149': 'emote'
                    }
                };
            _0x1a1c8c['exports'] = _0x109274;
        },
        '00000004': function(_0x0000, _0x0000, _0x0000) {
            'use strict';
            var _0x563ec2 = _0x5466b4('00000000');

            var _0x400a94 = {
                'gun_template': {
                    'name': 'Template gun',
                    'type': 'gun',
                    'quality': 0x0,
                    'fireMode': 'auto',
                    'caseTiming': 'shoot',
                    'ammo': '9mm',
                    'ammoSpawnCount': 0x0,
                    'maxClip': 0x0,
                    'maxReload': 0x00,
                    'extendedClip': 0x00,
                    'extendedReload': 0x00,
                    'reloadTime': 0x0,
                    'fireDelay': 0.1,
                    'switchDelay': 0.75,
                    'barrelLength': 2.625,
                    'barrelOffset': 0x0,
                    'recoilTime': 0x250000000,
                    'moveSpread': 0x0,
                    'shotSpread': 0x0,
                    'bulletCount': 0x0,
                    'bulletType': 'bullet_template',
                    'bulletTypeBonus': 'bullet_template_bonus',
                    'headshotMult': 0x2,
                    'size': 'med',
                    'speed': {
                        'equip': 0x0,
                        'attack': 0x0
                    },
                    'lootImg': {
                        'sprite': 'loot-weapon-mp5.img',
                        'tint': 0xff00,
                        'border': 'loot-circle-outer-01.img',
                        'borderTint': 0x0,
                        'scale': 0.3
                    },
                    'worldImg': {
                        'sprite': 'gun-med-01.img',
                        'scale': {
                            'x': 0.5,
                            'y': 0.49
                        },
                        'tint': 0x121212,
                        'leftHandOffset': {
                            'x': 0x0,
                            'y': 0x0
                        },
                        'recoil': 0x1
                    },
                    'particle': {
                        'shellScale': 0x1,
                        'shellOffset': 0.375
                    },
                    'sound': {
                        'shoot': 'mp5_01',
                        'reload': 'mp5_reload_01',
                        'pickup': 'gun_pickup_01',
                        'empty': 'empty_fire_01',
                        'deploy': 'mp5_switch_01'
                    }
                },
                'bugle': {
                    'name': 'Bugle',
                    'type': 'gun',
                    'quality': 0x0,
                    'fireMode': 'single',
                    'caseTiming': 'shoot',
                    'noDrop': true,
                    'noPotatoSwap': true,
                    'pistol': true,
                    'ignoreDetune': true,
                    'ammo': 'bugle_ammo',
                    'ammoSpawnCount': 0x0,
                    'maxClip': 0x1,
                    'maxReload': 0x1,
                    'extendedClip': 0x4,
                    'extendedReload': 0x1,
                    'reloadTime': 0.01,
                    'fireDelay': 0x1,
                    'switchDelay': 0.3,
                    'barrelLength': 0x3,
                    'barrelOffset': 0x0,
                    'recoilTime': 0x2540be400,
                    'moveSpread': 0x1,
                    'shotSpread': 0x1,
                    'bulletCount': 0x1,
                    'bulletType': 'bullet_bugle',
                    'noSplinter': true,
                    'headshotMult': 0x1,
                    'speed': {
                        'equip': 0x0,
                        'attack': 0x0
                    },
                    'lootImg': {
                        'sprite': 'loot-weapon-bugle.img',
                        'tint': 0xff00,
                        'border': 'loot-circle-outer-01.img',
                        'borderTint': 0x0,
                        'scale': 0.3
                    },
                    'worldImg': {
                        'sprite': 'gun-bugle-01.img',
                        'scale': {
                            'x': 0.5,
                            'y': 0.5
                        },
                        'tint': 0xffffff,
                        'leftHandOffset': {
                            'x': 0xc,
                            'y': 0x0
                        },
                        'recoil': 0x4
                    },
                    'particle': {
                        'shellScale': 0x4,
                        'shellOffset': 0x2,
                        'shellForward': 0x1
                    },
                    'sound': {
                        'shoot': 'bugle_01',
                        'shootTeam': {
                            0x1: 'bugle_01',
                            0x2: 'bugle_02'
                        },
                        'shootAlt': 'bugle_03',
                        'reload': '',
                        'pickup': 'stow_weapon_01',
                        'empty': 'empty_fire_01',
                        'deploy': 'stow_weapon_01'
                    }
                },
                'vss': {
                    'name': 'VSS',
                    'type': 'gun',
                    'quality': 0x1,
                    'fireMode': 'single',
                    'caseTiming': 'shoot',
                    'ammo': '9mm',
                    'ammoSpawnCount': 0x3c,
                    'maxClip': 0x14,
                    'maxReload': 0x14,
                    'extendedClip': 0x1e,
                    'extendedReload': 0x1e,
                    'reloadTime': 2.3,
                    'fireDelay': 0.16,
                    'switchDelay': 0.75,
                    'barrelLength': 3.7,
                    'barrelOffset': 0x0,
                    'recoilTime': 0x2540be400,
                    'moveSpread': 0x3,
                    'shotSpread': 0x2,
                    'bulletCount': 0x1,
                    'bulletType': 'bullet_vss',
                    'bulletTypeBonus': 'bullet_vss_bonus',
                    'headshotMult': 0x2,
                    'speed': {
                        'equip': 0x0,
                        'attack': 0x0
                    },
                    'lootImg': {
                        'sprite': 'loot-weapon-vss.img',
                        'tint': 0xff00,
                        'border': 'loot-circle-outer-01.img',
                        'borderTint': 0x0,
                        'scale': 0.3
                    },
                    'worldImg': {
                        'sprite': 'gun-vss-01.img',
                        'scale': {
                            'x': 0.5,
                            'y': 0.5
                        },
                        'tint': 0xffffff,
                        'leftHandOffset': {
                            'x': 0x9,
                            'y': 0x0
                        },
                        'recoil': 0x1
                    },
                    'particle': {
                        'shellScale': 0x1,
                        'shellOffset': 0.375
                    },
                    'sound': {
                        'shoot': 'vss_01',
                        'reload': 'vss_reload_01',
                        'pickup': 'gun_pickup_01',
                        'empty': 'empty_fire_01',
                        'deploy': 'vss_switch_01',
                        'fallOff': 0x3
                    }
                }
            };
            _0x1e5929['exports'] = _0x400a94;
        },
        '00000005': function(_0x5dc2f0, _0x5bf072, _0x132d29) {
            'use strict';
            var _0xec9522 = _0x132d29('00000006'),
                _0x202126 = _0x132d29('00000007'),
                _0x25d058 = 'production' === 'dev',
                _0x3aa887 = _0x132d29('fffffffe');
        },
        '00000006': function(_0x0000, _0x0000, _0x0000) {
            'use strict';

            var _0x0000a0 = function() {
                console.log("Some data")
            }
        },
        '00000007': function(_0x0000, _0x0000, _0x0000) {
            'use strict';
            var _0x3bdfba = _0xf7ddc9('6b42806d'),
                _0x9817dc = _0xf7ddc9('1901e2d9'),
                _0x2fc636 = _0xf7ddc9('c2a798c8');

            // Order of functions:
            // _0x4ac131 loot table insertions
            // _0x5b3eae specific items
            // _0x380b05 weighted random
            // _0x22121c recoloured sprites
            // _0x9f6cfb materials
            // _0xe2ffd6 barrels
            // _0x33a134 shipping container

            function _0x4ac131(_0xeef865, _0x462462, _0x11e5a5, _0x391bb5) {
                return _0x391bb5 = _0x391bb5 || {}, {
                    'tier': _0xeef865,
                    'min': _0x462462,
                    'max': _0x11e5a5,
                    'props': _0x391bb5
                };
            }

            function _0x5b3eae(_0x22d6c6, _0x3ddfe1, _0x32d30e) {
                return _0x32d30e = _0x32d30e || {}, {
                    'type': _0x22d6c6,
                    'count': _0x3ddfe1,
                    'props': _0x32d30e
                };
            }

            function _0x380b05(_0x5c26a5) {
                var _0x1a83a4 = [];
                for (var _0x7f692c in _0x5c26a5) {
                    _0x5c26a5['hasOwnProperty'](_0x7f692c) && _0x1a83a4['push']({
                        'type': _0x7f692c,
                        'weight': _0x5c26a5[_0x7f692c]
                    });
                }
                if (_0x1a83a4['length'] == 0) throw new Error('Invalid obstacle types');
                var _0x9907bb = 0;
                for (var _0x361f8e = 0; _0x361f8e < _0x1a83a4['length']; _0x361f8e++) {
                    _0x9907bb += _0x1a83a4[_0x361f8e]['weight'];
                }
                return function() {
                    var _0x2bda6f = _0x213555['random'](0, _0x9907bb),
                        _0x1e17b4 = 0;
                    while (_0x2bda6f > _0x1a83a4[_0x1e17b4]['weight']) {
                        _0x2bda6f -= _0x1a83a4[_0x1e17b4]['weight'], _0x1e17b4++;
                    }
                    return _0x1a83a4[_0x1e17b4]['type'];
                };
            }

            function _0x22121c(_0x42474b, _0x209b22, _0x48828d, _0x572413) {
                return {
                    'sprite': _0x42474b,
                    'scale': 0.5,
                    'alpha': _0x48828d || 1,
                    'tint': _0x209b22 || 16777215,
                    'zIdx': _0x572413 || 10
                };
            }
            var _0x9f6cfb = {
                'metal': {
                    'destructible': false,
                    'reflectBullets': true,
                    'hitParticle': 'barrelChip',
                    'explodeParticle': 'barrelBreak',
                    'sound': {
                        'bullet': 'wall_bullet',
                        'punch': 'metal_punch',
                        'explode': 'barrel_break_01',
                        'enter': 'none'
                    }
                },
                'wood': {
                    'destructible': true,
                    'reflectBullets': false,
                    'sound': {
                        'bullet': 'wall_wood_bullet',
                        'punch': 'wall_wood_bullet',
                        'explode': 'wall_break_01',
                        'enter': 'none'
                    }
                },
                'woodPerm': {
                    'destructible': false,
                    'reflectBullets': false,
                    'sound': {
                        'bullet': 'wall_wood_bullet',
                        'punch': 'wall_wood_bullet',
                        'explode': 'wall_break_01',
                        'enter': 'none'
                    }
                },
                'brick': {
                    'destructible': false,
                    'reflectBullets': false,
                    'hitParticle': 'brickChip',
                    'sound': {
                        'bullet': 'wall_brick_bullet',
                        'punch': 'wall_brick_bullet',
                        'explode': 'wall_break_01',
                        'enter': 'none'
                    }
                },
                'concrete': {
                    'destructible': false,
                    'reflectBullets': false,
                    'hitParticle': 'barrelChip',
                    'sound': {
                        'bullet': 'concrete_hit',
                        'punch': 'concrete_hit',
                        'explode': 'wall_break_01',
                        'enter': 'none'
                    }
                },
                'stone': {
                    'destructible': true,
                    'stonePlated': true,
                    'reflectBullets': false,
                    'hitParticle': 'rockChip',
                    'explodeParticle': 'rockBreak',
                    'sound': {
                        'bullet': 'concrete_hit',
                        'punch': 'concrete_hit',
                        'explode': 'stone_break_01',
                        'enter': 'none'
                    }
                },
                'glass': {
                    'destructible': true,
                    'reflectBullets': false,
                    'hitParticle': 'glassChip',
                    'explodeParticle': 'windowBreak',
                    'sound': {
                        'bullet': 'glass_bullet',
                        'punch': 'glass_bullet',
                        'explode': 'window_break_01',
                        'enter': 'none'
                    }
                },
                'cobalt': {
                    'destructible': false,
                    'reflectBullets': true,
                    'hitParticle': 'barrelChip',
                    'explodeParticle': 'barrelBreak',
                    'sound': {
                        'bullet': 'cobalt_bullet',
                        'punch': 'cobalt_bullet',
                        'explode': 'barrel_break_01',
                        'enter': 'none'
                    }
                }
            };

            function _0xe2ffd6(_0x58dfa3) {
                var _0x1ea7ef = {
                    'type': 'obstacle',
                    'obstacleType': 'barrel',
                    'scale': {
                        'createMin': 0x1,
                        'createMax': 0x1,
                        'destroy': 0.6
                    },
                    'collision': _0x19cb9e['createCircle'](_0x35fefc['create'](0, 0), 1.75),
                    'height': 0.5,
                    'collidable': true,
                    'destructible': true,
                    'explosion': 'explosion_barrel',
                    'health': 0x96,
                    'hitParticle': 'barrelChip',
                    'explodeParticle': 'barrelBreak',
                    'reflectBullets': true,
                    'loot': [],
                    'map': {
                        'display': true,
                        'color': 0x626262,
                        'scale': 0x1
                    },
                    'terrain': {
                        'grass': true,
                        'beach': true
                    },
                    'img': {
                        'sprite': 'map-barrel-01.img',
                        'scale': 0.4,
                        'alpha': 0x1,
                        'tint': 0xffffff,
                        'zIdx': 0xa
                    },
                    'sound': {
                        'bullet': 'barrel_bullet',
                        'punch': 'barrel_bullet',
                        'explode': 'barrel_break_01',
                        'enter': 'none'
                    }
                };
                return _0x213555['mergeDeep'](_0x1ea7ef, _0x58dfa3 || {});
            }

            function _0x1c5198(_0x585235) {
                var _0x7239df = {
                    'type': 'obstacle',
                    'scale': {
                        'createMin': 0x1,
                        'createMax': 0x1,
                        'destroy': 0x1
                    },
                    'collision': _0x19cb9e['createAabbExtents'](_0x35fefc['create'](0, 0), _0x35fefc['copy'](_0x585235['extents'])),
                    'height': 0xa,
                    'isWall': true,
                    'collidable': true,
                    'destructible': true,
                    'health': _0x585235['health'] || 150,
                    'hitParticle': 'woodChip',
                    'explodeParticle': 'woodPlank',
                    'reflectBullets': false,
                    'loot': [],
                    'map': {
                        'display': false
                    },
                    'img': {},
                    'sound': {
                        'bullet': 'wall_bullet',
                        'punch': 'wall_bullet',
                        'explode': 'barrel_break_01',
                        'enter': 'none'
                    }
                };
                if (!_0x9f6cfb[_0x585235['material']]) throw new Error('Invalid material ' + _0x585235['material']);
                return _0x213555['mergeDeep'](_0x7239df, _0x9f6cfb[_0x585235['material']], _0x585235 || {});
            }

            function _0x147376(_0x2b1106) {
                var _0x418c66 = {
                    'type': 'obstacle',
                    'obstacleType': 'locker',
                    'scale': {
                        'createMin': 0x1,
                        'createMax': 0x1,
                        'destroy': 0x1
                    },
                    'collision': _0x19cb9e['createAabbExtents'](_0x35fefc['create'](0, 0.15), _0x35fefc['create'](2.5, 1)),
                    'height': 0xa,
                    'collidable': true,
                    'destructible': true,
                    'health': 0x14,
                    'hitParticle': 'barrelChip',
                    'explodeParticle': 'depositBoxGreyBreak',
                    'reflectBullets': true,
                    'loot': [_0x4ac131('tier_world', 1, 1)],
                    'lootSpawn': {
                        'offset': _0x35fefc['create'](0, -1),
                        'speedMult': 0x0
                    },
                    'map': {
                        'display': false,
                        'color': 0x663300,
                        'scale': 0.875
                    },
                    'terrain': {
                        'grass': false,
                        'beach': true
                    },
                    'img': {
                        'sprite': 'map-deposit-box-01.img',
                        'residue': 'none',
                        'scale': 0.5,
                        'alpha': 0x1,
                        'tint': 0xffffff,
                        'zIdx': 0xa
                    },
                    'sound': {
                        'bullet': 'wall_bullet',
                        'punch': 'metal_punch',
                        'explode': 'deposit_box_break_01',
                        'enter': 'none'
                    }
                };
                return _0x213555['mergeDeep'](_0x418c66, _0x2b1106 || {});
            }

            function _0x33a134(_0x8b8b) {
                var _0x2411ec = [{
                        'type': 'container_wall_top',
                        'pos': _0x35fefc['create'](0, 7.95),
                        'scale': 0x1,
                        'ori': 0x0
                    }, {
                        'type': 'container_wall_side',
                        'pos': _0x35fefc['create'](2.35, 2.1),
                        'scale': 0x1,
                        'ori': 0x0
                    }, {
                        'type': 'container_wall_side',
                        'pos': _0x35fefc['create'](-2.35, 2.1),
                        'scale': 0x1,
                        'ori': 0x0
                    }, {
                        'type': _0x8b8b['loot_spawner_01'] || 'loot_tier_2',
                        'pos': _0x35fefc['create'](0, 3.25),
                        'scale': 0x1,
                        'ori': 0x0
                    }, {
                        'type': _0x8b8b['loot_spawner_02'] || _0x380b05({
                            'loot_tier_1': 0x2,
                            '': 0x1
                        }),
                        'pos': _0x35fefc['create'](0, 0.05),
                        'scale': 0x1,
                        'ori': 0x0
                    }],
                    _0x341ed0 = [{
                        'type': 'container_wall_side_open',
                        'pos': _0x35fefc['create'](2.35, 0),
                        'scale': 0x1,
                        'ori': 0x0
                    }, {
                        'type': 'container_wall_side_open',
                        'pos': _0x35fefc['create'](-2.35, 0),
                        'scale': 0x1,
                        'ori': 0x0
                    }, {
                        'type': 'loot_tier_2',
                        'pos': _0x35fefc['create'](0, -0.05),
                        'scale': 0x1,
                        'ori': 0x0
                    }, {
                        'type': _0x380b05({
                            'loot_tier_1': 0x1,
                            '': 0x1
                        }),
                        'pos': _0x35fefc['create'](0, 0.05),
                        'scale': 0x1,
                        'ori': 0x0
                    }];
                return {
                    'type': 'building',
                    'map': {
                        'display': true,
                        'color': _0x8b8b['mapTint'] || 2703694,
                        'scale': 0x1
                    },
                    'terrain': {
                        'grass': true,
                        'beach': true,
                        'riverShore': true
                    },
                    'zIdx': 0x1,
                    'floor': {
                        'surfaces': [{
                            'type': 'container',
                            'collision': [_0x8b8b['open'] ? _0x19cb9e['createAabbExtents'](_0x35fefc['create'](0, 0), _0x35fefc['create'](2.5, 11)) : _0x19cb9e['createAabbExtents'](_0x35fefc['create'](0, 0), _0x35fefc['create'](2.5, 8))]
                        }],
                        'imgs': [{
                            'sprite': _0x8b8b['open'] ? 'map-building-container-open-floor.img' : 'map-building-container-floor-01.img',
                            'scale': 0.5,
                            'alpha': 0x1,
                            'tint': _0x8b8b['tint']
                        }]
                    },
                    'ceiling': {
                        'zoomRegions': [{
                            'zoomIn': _0x8b8b['open'] ? _0x19cb9e['createAabbExtents'](_0x35fefc['create'](0, 0), _0x35fefc['create'](2.5, 5.75)) : _0x19cb9e['createAabbExtents'](_0x35fefc['create'](0, 2.25), _0x35fefc['create'](2.5, 5.5)),
                            'zoomOut': _0x8b8b['open'] ? _0x19cb9e['createAabbExtents'](_0x35fefc['create'](0, 0), _0x35fefc['create'](2.5, 11)) : _0x19cb9e['createAabbExtents'](_0x35fefc['create'](0, -0.5), _0x35fefc['create'](2.5, 8.75))
                        }],
                        'imgs': _0x8b8b['ceilingImgs'] || [{
                            'sprite': _0x8b8b['ceilingSprite'],
                            'scale': 0.5,
                            'alpha': 0x1,
                            'tint': _0x8b8b['tint']
                        }]
                    },
                    'mapObjects': _0x8b8b['open'] ? _0x341ed0 : _0x2411ec
                };
            }
            var _0x2f9447 = {
                'hut_wall_int_4': _0x1c5198({
                    'material': 'wood',
                    'extents': _0x35fefc['create'](0.5, 2),
                    'hitParticle': 'tanChip',
                    'img': _0x22121c('map-wall-04.img', 4608000)
                }),
                'deposit_box_01': _0x147376({
                    'img': {
                        'sprite': 'map-deposit-box-01.img'
                    },
                    'loot': [_0x4ac131('tier_world', 1, 1)]
                }),
                'barrel_01b': _0xe2ffd6({
                    'img': {
                        'tint': 0xc9c9c9
                    },
                    'loot': [_0x4ac131('tier_surviv', 2, 3), _0x5b3eae('mirv', 1), _0x5b3eae('mirv', 1), _0x5b3eae('mirv', 1)]
                }),
                'container_01': _0x33a134({
                    'open': false,
                    'tint': 0x29414e,
                    'ceilingSprite': 'map-building-container-ceiling-01.img'
                }),
                'destructible_filler': {
                    'destructible0': 'destructible',
                    'destructible1': 'destructible',
                    'destructible2': 'destructible',
                    'destructible3': 'destructible',
                    'destructible4': 'destructible',
                    'destructible5': 'destructible',
                    'destructible6': 'destructible',
                    'destructible7': 'destructible',
                    'destructible8': 'destructible',
                    'destructible9': 'destructible',
                    'destructible10': 'destructible',
                    'destructible11': 'destructible',
                    'destructible12': 'destructible',
                    'destructible13': 'destructible',
                    'destructible14': 'destructible',
                    'destructible15': 'destructible',
                    'destructible16': 'destructible',
                    'destructible17': 'destructible',
                    'destructible18': 'destructible',
                    'destructible19': 'destructible'
                }
            };

        },
        '00000008': function(_0x5efe1e, _0x0000, _0x0000) {
            'use strict';
            _0x5efe1e['exports'] = {
                'protocolVersion': 0x6d,
                'clientVersion': '1.7.0c',
                'Input': {
                    'MoveLeft': 0x0,
                    'MoveRight': 0x1,
                    'MoveUp': 0x2,
                    'MoveDown': 0x3,
                    'Fire': 0x4,
                    'Reload': 0x5,
                    'Cancel': 0x6,
                    'Interact': 0x7,
                    'Revive': 0x8,
                    'Use': 0x9,
                    'Loot': 0xa,
                    'EquipPrimary': 0xb,
                    'EquipSecondary': 0xc,
                    'EquipMelee': 0xd,
                    'EquipThrowable': 0xe,
                    'EquipFragGrenade': 0xf,
                    'EquipSmokeGrenade': 0x10,
                    'EquipNextWeap': 0x11,
                    'EquipPrevWeap': 0x12,
                    'EquipLastWeap': 0x13,
                    'EquipOtherGun': 0x14,
                    'EquipPrevScope': 0x15,
                    'EquipNextScope': 0x16,
                    'UseBandage': 0x17,
                    'UseHealthKit': 0x18,
                    'UseSoda': 0x19,
                    'UsePainkiller': 0x1a,
                    'StowWeapons': 0x1b,
                    'SwapWeapSlots': 0x1c,
                    'ToggleMap': 0x1d,
                    'CycleUIMode': 0x1e,
                    'EmoteMenu': 0x1f,
                    'TeamPingMenu': 0x20,
                    'Fullscreen': 0x21,
                    'HideUI': 0x22,
                    'TeamPingSingle': 0x23,
                    'UseEventItem': 0x24,
                    'Count': 0x25
                },
                'EmoteSlot': {
                    'Top': 0x0,
                    'Right': 0x1,
                    'Bottom': 0x2,
                    'Left': 0x3,
                    'Win': 0x4,
                    'Death': 0x5,
                    'Count': 0x6
                },
                'WeaponSlot': {
                    'Primary': 0x0,
                    'Secondary': 0x1,
                    'Melee': 0x2,
                    'Throwable': 0x3,
                    'Count': 0x4
                },
                'WeaponType': ['gun', 'gun', 'melee', 'throwable'],
                'DamageType': {
                    'Player': 0x0,
                    'Bleeding': 0x1,
                    'Gas': 0x2,
                    'Airdrop': 0x3,
                    'Airstrike': 0x4,
                    'Freeze': 0x5,
                    'Weather': 0x6,
                    'Npc': 0x7,
                    'Burning': 0x8,
                    'Phoenix': 0x9
                },
                'Action': {
                    'None': 0x0,
                    'Reload': 0x1,
                    'ReloadAlt': 0x2,
                    'UseItem': 0x3,
                    'Revive': 0x4
                },
                'Anim': {
                    'None': 0x0,
                    'Melee': 0x1,
                    'Cook': 0x2,
                    'Throw': 0x3,
                    'CrawlForward': 0x4,
                    'CrawlBackward': 0x5,
                    'Revive': 0x6,
                    'ChangePose': 0x7
                },
                'GasMode': {
                    'Inactive': 0x0,
                    'Waiting': 0x1,
                    'Moving': 0x2
                },
                'Plane': {
                    'Airdrop': 0x0,
                    'Airstrike': 0x1
                },
                'HasteType': {
                    'None': 0x0,
                    'Windwalk': 0x1,
                    'Takedown': 0x2,
                    'Inspire': 0x3
                },
                'map': {
                    'gridSize': 0x10,
                    'shoreVariation': 0x3,
                    'grassVariation': 0x2
                },
                'player': {
                    'radius': 0x1,
                    'maxVisualRadius': 3.75,
                    'maxInteractionRad': 3.5,
                    'health': 0x64,
                    'reviveHealth': 0x18,
                    'boostBreakpoints': [1, 1, 1.5, 0.5],
                    'baseSwitchDelay': 0.25,
                    'freeSwitchCooldown': 0x1,
                    'bleedTickRate': 0x1,
                    'reviveDuration': 0x8,
                    'reviveRange': 0x5,
                    'crawlTime': 0.75,
                    'emoteSoftCooldown': 0x2,
                    'emoteHardCooldown': 0x6,
                    'emoteThreshold': 0x6,
                    'throwableMaxMouseDist': 0x12,
                    'cookTime': 0.1,
                    'throwTime': 0.3,
                    'meleeHeight': 0.25,
                    'touchLootRadMult': 1.4,
                    'medicHealRange': 0x8,
                    'medicReviveRange': 0x6
                },
                'defaultEmoteLoadout': ['emote_happyface', 'emote_thumbsup', 'emote_surviv', 'emote_sadface', '', ''],
                'airdrop': {
                    'actionOffset': 0x0,
                    'fallTime': 0x8,
                    'crushDamage': 0x64,
                    'planeVel': 0x30,
                    'planeRad': 0x96,
                    'soundRangeMult': 2.5,
                    'soundRangeDelta': 0.25,
                    'soundRangeMax': 0x5c,
                    'fallOff': 0x0
                },
                'airstrike': {
                    'actionOffset': 0x0,
                    'bombJitter': 0x4,
                    'bombOffset': 0x2,
                    'bombVel': 0x3,
                    'bombCount': 0x14,
                    'planeVel': 0x15e,
                    'planeRad': 0x78,
                    'soundRangeMult': 0x12,
                    'soundRangeDelta': 0x12,
                    'soundRangeMax': 0x30,
                    'fallOff': 1.25
                },
                'groupColors': [16776960, 16711935, 65535, 16733184],
                'teamColors': [13369344, 32511],
                'bullet': {
                    'maxReflect': 0x3,
                    'reflectDistDecay': 1.5,
                    'height': 0.25
                },
                'projectile': {
                    'maxHeight': 0x5
                },
                'structureLayerCount': 0x2,
                'tracerColors': {
                    '9mm': {
                        'regular': 0xfee2c6,
                        'saturated': 0xffd9b3,
                        'chambered': 0xff7f00,
                        'alphaRate': 0.92,
                        'alphaMin': 0.14
                    },
                    '9mm_suppressed_bonus': {
                        'regular': 0xfee2c6,
                        'saturated': 0xffd9b3,
                        'chambered': 0xff7f00,
                        'alphaRate': 0.96,
                        'alphaMin': 0.28
                    },
                    '9mm_cursed': {
                        'regular': 0x130900,
                        'saturated': 0x130900,
                        'chambered': 0x130900,
                        'alphaRate': 0.92,
                        'alphaMin': 0.14
                    },
                    '762mm': {
                        'regular': 0xc5d6fe,
                        'saturated': 0xabc4ff,
                        'chambered': 0x4cff,
                        'alphaRate': 0.94,
                        'alphaMin': 0.2
                    },
                    '12gauge': {
                        'regular': 0xfedcdc,
                        'saturated': 0xfedcdc,
                        'chambered': 0xff0000
                    },
                    'laser': {
                        'regular': 0xff0000,
                        'saturated': 0xff0000,
                        'chambered': 0xff0000
                    },
                    'water': {
                        'regular': 0x3771fa,
                        'saturated': 0x3771fa,
                        'chambered': 0x3771fa
                    },
                    '556mm': {
                        'regular': 0xa9ff92,
                        'saturated': 0xa9ff92,
                        'chambered': 0x36ff00,
                        'alphaRate': 0.92,
                        'alphaMin': 0.14
                    },
                    '50AE': {
                        'regular': 0xfff088,
                        'saturated': 0xfff088,
                        'chambered': 0xffdf00
                    },
                    '308sub': {
                        'regular': 0x252b00,
                        'saturated': 0x465000,
                        'chambered': 0x131600,
                        'alphaRate': 0.92,
                        'alphaMin': 0.07
                    },
                    'flare': {
                        'regular': 0xe2e2e2,
                        'saturated': 0xe2e2e2,
                        'chambered': 0xc4c4c4
                    },
                    '45acp': {
                        'regular': 0xecbeff,
                        'saturated': 0xe7acff,
                        'chambered': 0xb500ff
                    },
                    'shrapnel': {
                        'regular': 0x333333,
                        'saturated': 0x333333
                    },
                    'frag': {
                        'regular': 0xcb0000,
                        'saturated': 0xcb0000
                    },
                    'invis': {
                        'regular': 0x0,
                        'saturated': 0x0,
                        'chambered': 0x0
                    },
                    'heart': {
                        'regular': 0xfee2c6,
                        'saturated': 0xffd9b3,
                        'chambered': 0xff7f00,
                        'alphaRate': 0.92,
                        'alphaMin': 0.14
                    },
                    'blackTrail': {
                        'regular': 0x0,
                        'saturated': 0x0,
                        'chambered': 0x0,
                        'alphaRate': 0.92,
                        'alphaMin': 0.14
                    },
                    'rainbowTrail': {
                        'regular': 0xffffff,
                        'saturated': 0xffffff,
                        'chambered': 0xffffff,
                        'alphaRate': 0.92,
                        'alphaMin': 0.14
                    },
                    'skitternade': {
                        'regular': 0x9bff99,
                        'saturated': 0x9bff99,
                        'chambered': 0x9bff99
                    },
                    'antiFire': {
                        'regular': 0x9bff99,
                        'saturated': 0x9bff99,
                        'chambered': 0x9bff99
                    }
                },
                'scopeZoomRadius': {
                    'desktop': {
                        '1xscope': 0x1c,
                        '2xscope': 0x24,
                        '4xscope': 0x30,
                        '8xscope': 0x44,
                        '15xscope': 0x68
                    },
                    'mobile': {
                        '1xscope': 0x20,
                        '2xscope': 0x28,
                        '4xscope': 0x30,
                        '8xscope': 0x40,
                        '15xscope': 0x58
                    }
                },
                'bagSizes': {
                    '9mm': [120, 240, 330, 420],
                    '762mm': [90, 180, 240, 300],
                    '556mm': [90, 180, 240, 300],
                    '12gauge': [15, 30, 60, 90],
                    '50AE': [49, 98, 147, 196],
                    '308sub': [10, 20, 40, 80],
                    'flare': [2, 4, 6, 8],
                    '40mm': [10, 20, 30, 40],
                    '45acp': [90, 180, 240, 300],
                    'mine': [3, 6, 9, 12],
                    'frag': [3, 6, 9, 12],
                    'heart_frag': [3, 6, 9, 12],
                    'smoke': [3, 6, 9, 12],
                    'strobe': [2, 3, 4, 5],
                    'mirv': [2, 4, 6, 8],
                    'snowball': [10, 20, 30, 40],
                    'water_balloon': [10, 20, 30, 40],
                    'skitternade': [10, 20, 30, 40],
                    'antiFire': [10, 20, 30, 40],
                    'potato': [10, 20, 30, 40],
                    'bandage': [5, 10, 15, 30],
                    'healthkit': [1, 2, 3, 4],
                    'soda': [2, 5, 10, 15],
                    'chocolateBox': [2, 5, 10, 15],
                    'bottle': [2, 5, 10, 15],
                    'gunchilada': [2, 5, 10, 15],
                    'watermelon': [2, 5, 10, 15],
                    'nitroLace': [2, 5, 10, 15],
                    'flask': [2, 5, 10, 15],
                    'pulseBox': [2, 5, 10, 15],
                    'painkiller': [1, 2, 3, 4],
                    '1xscope': [1, 1, 1, 1],
                    '2xscope': [1, 1, 1, 1],
                    '4xscope': [1, 1, 1, 1],
                    '8xscope': [1, 1, 1, 1],
                    '15xscope': [1, 1, 1, 1],
                    'rainbow_ammo': [1, 1, 1, 1]
                },
                'lootRadius': {
                    'outfit': 0x1,
                    'melee': 1.25,
                    'gun': 1.25,
                    'throwable': 0x1,
                    'ammo': 1.2,
                    'heal': 0x1,
                    'boost': 0x1,
                    'backpack': 0x1,
                    'helmet': 0x1,
                    'chest': 0x1,
                    'scope': 0x1,
                    'perk': 1.25,
                    'xp': 0x1
                },
                'features': {
                    'inGameNotificationActive': true,
                    'collectClientMetrics': false
                }
            };
        },
        '00000009': function(_0xbb5d02, _0x3f952c, _0x401fe6) {
            'use strict';
            var _0x495880 = {
                'main': _0x401fe6('00000010'),
                'main_spring': _0x401fe6('00000011'),
                'main_summer': _0x401fe6('00000012'),
                'woods': _0x401fe6('00000013'),
                'woods_snow': _0x401fe6('00000014'),
                'woods_spring': _0x401fe6('00000015'),
                'storm': _0x401fe6('00000016'),
                'contact': _0x401fe6('00000017')
            };
            _0xbb5d02['exports'] = _0x495880;
        },
        '00000010': function(_0x213f02, _0x5ac8e6, _0x34cd36) {
            'use strict';
            var _0x30e509 = _0x34cd36('989ad62a'),
                _0x3fae9e = _0x34cd36('c2a798c8'),
                _0x5cb5ea = {
                    'mapId': 0x0,
                    'desc': {
                        'name': 'Normal',
                        'icon': 'img/gui/emote.svg',
                        'buttonCss': '',
                        'buttonText': 'index-play-mode-main'
                    },
                    'assets': {
                        'audio': [{
                            'name': 'club_music_01',
                            'channel': 'ambient'
                        }, {
                            'name': 'club_music_02',
                            'channel': 'ambient'
                        }, {
                            'name': 'ambient_steam_01',
                            'channel': 'ambient'
                        }],
                        'atlases': ['gradient', 'loadout', 'loadout2', 'shared', 'main']
                    },
                    'biome': {
                        'colors': {
                            'background': 0x20536e,
                            'water': 0x3282ab,
                            'waterRipple': 0xb3f0ff,
                            'beach': 0xcdb35b,
                            'riverbank': 0x905e24,
                            'grass': 0x80af49,
                            'underground': 0x1b0d03,
                            'playerSubmerge': 0x2b8ca4,
                            'playerGhillie': 0x83af50
                        },
                        'valueAdjust': 0x1,
                        'sound': {
                            'riverShore': 'sand'
                        },
                        'particles': {
                            'camera': ''
                        },
                        'tracerColors': {},
                        'airdrop': {
                            'planeImg': 'map-plane-01.img',
                            'planeSound': 'plane_01',
                            'airdropImg': 'map-chute-01.img'
                        }
                    },
                    'gameMode': {
                        'maxPlayers': 0x50,
                        'killLeaderEnabled': true
                    }
                };
            _0x213f02['exports'] = _0x5cb5ea;
        },
        '00000011': function(_0x37cc22, _0x4ec92c, _0x5ad956) {
            'use strict';
            var _0x355ce0 = _0x5ad956('989ad62a'),
                _0x20779c = _0x5ad956('1901e2d9'),
                _0x2585c2 = _0x5ad956('c2a798c8'),
                _0x3caac3 = _0x5ad956('00000010'),
                _0x4b1e29 = {
                    'assets': {
                        'audio': [],
                        'atlases': ['gradient', 'loadout', 'loadout2', 'shared', 'main', 'valentine']
                    },
                    'desc': {
                        'name': 'Awesome Blossoms',
                        'icon': 'img/loot/loot-blossom-icon.svg',
                        'buttonCss': 'btn-mode-blossoms',
                        'buttonText': 'index-play-mode-spring'
                    },
                    'biome': {
                        'colors': {
                            'background': 0x20536e,
                            'water': 0x3282ab,
                            'waterRipple': 0xb3f0ff,
                            'beach': 0xf4ae48,
                            'riverbank': 0x8a8a8a,
                            'grass': 0x5c910a,
                            'underground': 0x1b0d03,
                            'playerSubmerge': 0x2b8ca4,
                            'playerGhillie': 0x41630a
                        },
                        'sound': {
                            'riverShore': 'stone'
                        },
                        'particles': {
                            'camera': 'falling_leaf_spring'
                        }
                    }
                };
            _0x37cc22['exports'] = _0x20779c['mergeDeep']({}, _0x3caac3, _0x4b1e29);
        },
        '00000012': function(_0x118ec4, _0x332057, _0x54a6f8) {
            'use strict';
            var _0x5a0f98 = _0x54a6f8('989ad62a'),
                _0x45a206 = _0x54a6f8('1901e2d9'),
                _0x39c225 = _0x54a6f8('c2a798c8'),
                _0x50a018 = _0x54a6f8('00000010'),
                _0x13aedd = {
                    'assets': {
                        'audio': [{
                            'name': 'club_music_01',
                            'channel': 'ambient'
                        }, {
                            'name': 'club_music_02',
                            'channel': 'ambient'
                        }, {
                            'name': 'ambient_steam_01',
                            'channel': 'ambient'
                        }],
                        'atlases': ['gradient', 'loadout', 'loadout2', 'shared', 'main']
                    },
                    'biome': {
                        'colors': {
                            'background': 0x20536e,
                            'water': 0x3282ab,
                            'waterRipple': 0xb3f0ff,
                            'beach': 0xdc9e28,
                            'riverbank': 0xa37119,
                            'grass': 0x629522,
                            'underground': 0x1b0d03,
                            'playerSubmerge': 0x2b8ca4,
                            'playerGhillie': 0x659825
                        }
                    }
                };
            _0x118ec4['exports'] = _0x45a206['mergeDeep']({}, _0x50a018, _0x13aedd);
        },
        '00000013': function(_0x411757, _0x2b05fa, _0x17e709) {
            'use strict';
            var _0x4643ee = _0x17e709('989ad62a'),
                _0x514c60 = _0x17e709('1901e2d9'),
                _0x5c5a54 = _0x17e709('c2a798c8'),
                _0x321022 = _0x17e709('00000010'),
                _0x4791e4 = {
                    'mapId': 0x2,
                    'desc': {
                        'name': 'Woods',
                        'icon': 'img/gui/player-king-woods.svg',
                        'buttonCss': 'btn-mode-woods',
                        'buttonText': 'index-play-mode-woods'
                    },
                    'assets': {
                        'audio': [{
                            'name': 'vault_change_02',
                            'channel': 'sfx'
                        }, {
                            'name': 'log_01',
                            'channel': 'sfx'
                        }, {
                            'name': 'log_02',
                            'channel': 'sfx'
                        }, {
                            'name': 'helmet03_forest_pickup_01',
                            'channel': 'ui'
                        }, {
                            'name': 'ability_stim_01',
                            'channel': 'sfx'
                        }, {
                            'name': 'leader_dead_01',
                            'channel': 'ui'
                        }],
                        'atlases': ['gradient', 'loadout', 'loadout2', 'shared', 'woods']
                    },
                    'biome': {
                        'colors': {
                            'background': 0x20536e,
                            'water': 0x3282ab,
                            'waterRipple': 0xb3f0ff,
                            'beach': 0xefb35b,
                            'riverbank': 0x77360b,
                            'grass': 0x8e832a,
                            'underground': 0x1b0d03,
                            'playerSubmerge': 0x2b8ca4
                        },
                        'particles': {
                            'camera': 'falling_leaf'
                        }
                    },
                    'gameMode': {
                        'maxPlayers': 0x50,
                        'woodsMode': true
                    }
                };
            _0x411757['exports'] = _0x514c60['mergeDeep']({}, _0x321022, _0x4791e4);
        },
        '00000014': function(_0x5c69b2, _0x2f96c6, _0x323ff0) {
            'use strict';
            var _0x156e23 = _0x323ff0('989ad62a'),
                _0x513e00 = _0x323ff0('1901e2d9'),
                _0x641e45 = _0x323ff0('c2a798c8'),
                _0xedda06 = _0x323ff0('00000013'),
                _0x350020 = {
                    'assets': {
                        'audio': [{
                            'name': 'vault_change_02',
                            'channel': 'sfx'
                        }, {
                            'name': 'footstep_08',
                            'channel': 'sfx'
                        }, {
                            'name': 'footstep_09',
                            'channel': 'sfx'
                        }, {
                            'name': 'helmet03_forest_pickup_01',
                            'channel': 'ui'
                        }, {
                            'name': 'ability_stim_01',
                            'channel': 'sfx'
                        }, {
                            'name': 'leader_dead_01',
                            'channel': 'ui'
                        }, {
                            'name': 'snowball_01',
                            'channel': 'sfx'
                        }, {
                            'name': 'snowball_02',
                            'channel': 'sfx'
                        }, {
                            'name': 'snowball_pickup_01',
                            'channel': 'ui'
                        }],
                        'atlases': ['gradient', 'loadout', 'loadout2', 'shared', 'woods', 'snow']
                    },
                    'biome': {
                        'colors': {
                            'background': 0x93639,
                            'water': 0xc4d51,
                            'waterRipple': 0xb3f0ff,
                            'beach': 0xcdb35b,
                            'riverbank': 0x905e24,
                            'grass': 0xbdbdbd,
                            'underground': 0x1b0d03,
                            'playerSubmerge': 0x2b8ca4
                        },
                        'particles': {
                            'camera': 'falling_snow_slow'
                        },
                        'tracerColors': {
                            '762mm': {
                                'regular': 0x96a1e6,
                                'saturated': 0xabc4ff,
                                'alphaRate': 0.96,
                                'alphaMin': 0.4
                            }
                        }
                    }
                };
            _0x5c69b2['exports'] = _0x513e00['mergeDeep']({}, _0xedda06, _0x350020);
        },
        '00000015': function(_0x10fb1e, _0x4e8375, _0x37a8fd) {
            'use strict';
            var _0x9584bf = _0x37a8fd('989ad62a'),
                _0x50d9de = _0x37a8fd('1901e2d9'),
                _0xa2acf1 = _0x37a8fd('c2a798c8'),
                _0x1ae455 = _0x37a8fd('00000013'),
                _0x28a28e = {
                    'biome': {
                        'colors': {
                            'background': 0x20536e,
                            'water': 0x3282ab,
                            'waterRipple': 0xb3f0ff,
                            'beach': 0xefb35b,
                            'riverbank': 0x8a8a8a,
                            'grass': 0x426609,
                            'underground': 0x1b0d03,
                            'playerSubmerge': 0x2b8ca4
                        },
                        'sound': {
                            'riverShore': 'stone'
                        },
                        'particles': {
                            'camera': 'falling_leaf_spring'
                        }
                    }
                };
            _0x10fb1e['exports'] = _0x50d9de['mergeDeep']({}, _0x1ae455, _0x28a28e);
        },
        '00000016': function(_0x474a29, _0x5cbcb0, _0x28f2af) {
            'use strict';
            var _0x43fa6c = _0x28f2af('989ad62a'),
                _0x4568b9 = _0x28f2af('1901e2d9'),
                _0x236fde = _0x28f2af('c2a798c8'),
                _0x3773fa = _0x28f2af('00000010'),
                _0x50a203 = {
                    'mapId': 0xf,
                    'desc': {
                        'name': 'Storm',
                        'icon': 'img/gui/storm-icon.svg',
                        'buttonCss': 'btn-mode-storm'
                    },
                    'assets': {
                        'audio': [{
                            'name': 'vault_change_02',
                            'channel': 'sfx'
                        }, {
                            'name': 'log_01',
                            'channel': 'sfx'
                        }, {
                            'name': 'log_02',
                            'channel': 'sfx'
                        }, {
                            'name': 'helmet03_forest_pickup_01',
                            'channel': 'ui'
                        }, {
                            'name': 'ability_stim_01',
                            'channel': 'sfx'
                        }, {
                            'name': 'leader_dead_01',
                            'channel': 'ui'
                        }],
                        'atlases': ['gradient', 'loadout', 'loadout2', 'shared', 'woods', 'storm']
                    },
                    'biome': {
                        'colors': {
                            'background': 0x20536e,
                            'water': 0x456971,
                            'waterRipple': 0xb3f0ff,
                            'beach': 0xefb35b,
                            'riverbank': 0x77360b,
                            'grass': 0x8e832a,
                            'underground': 0x1b0d03,
                            'playerSubmerge': 0x2b8ca4
                        },
                        'particles': {
                            'camera': 'falling_rain_fast'
                        }
                    },
                    'gameMode': {
                        'maxPlayers': 0x50,
                        'woodsMode': true,
                        'rainMode': true
                    }
                };
            _0x474a29['exports'] = _0x4568b9['mergeDeep']({}, _0x3773fa, _0x50a203);
        },
        '00000017': function(_0x368f04, _0x2d4068, _0x31a8ca) {
            'use strict';
            var _0x56f231 = _0x31a8ca('989ad62a'),
                _0x1b9d16 = _0x31a8ca('c2a798c8'),
                _0x330bdb = {
                    'mapId': 0x11,
                    'desc': {
                        'name': 'Contact',
                        'icon': 'img/loot/loot-contact.svg',
                        'buttonCss': 'btn-mode-contact',
                        'buttonText': 'index-play-mode-contact'
                    },
                    'assets': {
                        'audio': [{
                            'name': 'club_music_01',
                            'channel': 'ambient'
                        }, {
                            'name': 'club_music_02',
                            'channel': 'ambient'
                        }, {
                            'name': 'ambient_steam_01',
                            'channel': 'ambient'
                        }],
                        'atlases': ['gradient', 'loadout', 'loadout2', 'shared', 'main', 'contact']
                    },
                    'biome': {
                        'colors': {
                            'background': 0x20536e,
                            'water': 0x7f5fff,
                            'waterRipple': 0xb3f0ff,
                            'beach': 0x6774a1,
                            'riverbank': 0x4d5b8b,
                            'grass': 0x2d385d,
                            'underground': 0x1b0d03,
                            'playerSubmerge': 0x2b8ca4,
                            'playerGhillie': 0x83af50
                        },
                        'valueAdjust': 0x1,
                        'sound': {
                            'riverShore': 'sand'
                        },
                        'particles': {
                            'camera': ''
                        },
                        'tracerColors': {},
                        'airdrop': {
                            'planeImg': 'map-plane-01.img',
                            'planeSound': 'plane_01',
                            'airdropImg': 'map-chute-01.img'
                        }
                    },
                    'gameMode': {
                        'maxPlayers': 0x50,
                        'killLeaderEnabled': true,
                        'contactMode': true
                    }
                };
            _0x368f04['exports'] = _0x330bdb;
        },
        '00000018': function(_0x2e93f6, _0xe2e298, _0x163ed1) {
            'use strict';
            var _0xfe36e2 = _0x163ed1('f05b4d6a'),
                _0x5a7e54 = _0x25112d(_0xfe36e2);

            function _0x25112d(_0x543f7e) {
                return _0x543f7e && _0x543f7e['__esModule'] ? _0x543f7e : {
                    'default': _0x543f7e
                };
            }
            var _0x3e71d8 = _0x163ed1('00000019'),
                _0x5ada4c = {
                    'getProxyDef': function _0x1cc202() {
                        if (false) {}
                        var _0x45d20f = (0, _0x5a7e54['default'])(_0x3e71d8);
                        for (var _0x1937b0 = 0; _0x1937b0 < _0x45d20f['length']; _0x1937b0++) {
                            var _0x34ebe6 = _0x45d20f[_0x1937b0];
                            if (window['location']['hostname']['indexOf'](_0x34ebe6) !== -1) return {
                                'proxy': _0x34ebe6,
                                'def': _0x3e71d8[_0x34ebe6]
                            };
                        }
                        return null;
                    }
                };
        },
        '00000019': function(_0x49cd3c) {
            _0x49cd3c['exports'] = {
                "surviv.io": {
                    "all": true
                },
                "surviv2.io": {
                    "google": true,
                    "discord": true
                },
                "2dbattleroyale.com": {
                    "google": true,
                    "discord": true
                },
                "2dbattleroyale.org": {
                    "google": true,
                    "discord": true
                },
                "piearesquared.info": {
                    "google": true,
                    "discord": true
                },
                "thecircleisclosing.com": {
                    "google": true,
                    "discord": true
                },
                "secantsecant.com": {
                    "google": true,
                    "discord": true
                },
                "parmainitiative.com": {
                    "google": true,
                    "discord": true
                },
                "ot38.club": {
                    "google": true,
                    "discord": true
                },
                "drchandlertallow.com": {
                    "google": true,
                    "discord": true
                },
                "rarepotato.com": {
                    "google": true,
                    "discord": true
                },
                "archimedesofsyracuse.info": {
                    "google": true,
                    "discord": true
                },
                "nevelskoygroup.com": {
                    "google": true,
                    "discord": true
                },
                "kugahi.com": {
                    "google": true,
                    "discord": true
                },
                "kugaheavyindustry.com": {
                    "google": true,
                    "discord": true
                },
                "chandlertallowmd.com": {
                    "google": true,
                    "discord": true
                }
            };
        },
        'ffffffff': function(_0x0000, _0x0000, _0x0000) {
            'use strict';

        }
]);