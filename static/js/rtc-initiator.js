/************************** WEBRTC INITIATOR **************************/
function initializePeer () {
    console.log('Initializing Peer');
    const peer = new SimplePeer({
        config: {
            iceServers: [
                {
                    urls: [
                        'stun:stun.l.google.com:19302',
                        'stun:stun1.l.google.com:19302',
                        'stun:stun2.l.google.com:19302',
                        'stun:stun3.l.google.com:19302',
                        'stun:stun4.l.google.com:19302',
                        'stun:global.stun.twilio.com:3478'
                    ]
                },{
                    urls: [
                        'turn:relay.backups.cz',
                        'turn:relay.backups.cz?transport=tcp'
                    ],
                    credential: 'webrtc',
                    username: 'webrtc'
                }
            ]
        },
        initiator: true,
        trickle: false
    });
    /* Allow 'window' context to reference the function */
    window.peer = peer;

    peer.on('error', err => console.log('error', err));
    
    peer.on('signal', (data) => {
        console.log('Initiator Signaling Started');
        console.log(data);
        socket.emit('sendOfferToUser', JSON.stringify(data));
    });
    
    socket.on('receiveReceiverAnswer', (data) => {
        peer.signal(data);
    });
    
    peer.on('connect', () => {
        console.log('Initiator Connected');
        /***
         * 
         * - Welcome signal is sent after receiving the Receiver's Welcome Signal,
         * - this is done in order to validate if the user is anonymous or not
         * - so that we send the appropriate info to the user.
         * 
        ***/
    });
    
    function sentWelcomeData(anon = '') {
        let userData = swcms.advStreams.myUserInfo;
        
        if (anon == 'anonAgent') {
            userData.name = 'Agente Conecta';
            userData.photoURL = '/static/images/manifest/agent_f.svg';
        }
    
        peer.send(JSON.stringify({
            msgType: 'welcome',
            msgUserInfo: userData
        }));
    }
    
    peer.on('close', () => {
        console.log('Receiver Disconnected');
        let userName = document.querySelector('.container-chat--topbar-info-data-name').textContent;
        document.querySelector('.container-chat--topbar-info-data-status-icon').classList.remove('s-font-color-green-confirm');
        document.querySelector('.container-chat--topbar-info-data-status-icon').classList.add('s-font-color-secondary');
        document.querySelector('.container-chat--topbar-info-data-status-text').textContent = 'Offline';
        document.querySelector('.container-chat--topbar-info-data-status-text').classList.remove('s-font-color-primary');
        document.querySelector('.container-chat--topbar-info-data-status-text').classList.add('s-font-color-secondary');
        document.querySelector('.mdc-text-field--textarea').classList.add('mdc-text-field--disabled');
        document.querySelector('.mdc-text-field__input').disabled = true;
        document.querySelector('#audioCall').disabled = true;
        document.querySelector('#moreOptionsButton').disabled = true;
        document.querySelector('#videoCall').disabled = true;
        swcms.appendChatMessage(userName + ' Offline.', null, 'auto');
    });
    
    peer.on('data', (data) => {
        console.log('Initiator Data Received: ' + data);
        jMsg = JSON.parse(data);
        switch (jMsg.msgType) {
            case 'audio':
            case 'audiovideo':
                if (jMsg.msg == 'accepted') {
                    swcms.managePeerStream('send');
                } else if (jMsg.msg == 'ended') {
                    swcms.endAVCall(false);
                }
                swcms.displayCallUI(jMsg.msg, jMsg.msgType);
                break;
    
            case 'msg':
                swcms.appendChatMessage(jMsg.msg, jMsg.msgDateTime, 'others', jMsg.msgUserName);
                break;
    
            case 'welcome':
                if (jMsg.msgUserInfo.name == 'Anonim@') {
                    sentWelcomeData('anonAgent');
                } else {
                    sentWelcomeData();
                }
                swcms.advStreams.otherUserInfo = jMsg.msgUserInfo;
                document.querySelector('#chat-pic').src = jMsg.msgUserInfo.photoURL;
                document.querySelector('#callerid-pic').src = jMsg.msgUserInfo.photoURL;
                document.querySelector('#callerid-name').textContent = jMsg.msgUserInfo.name;
                document.querySelector('.container-chat--topbar-info-data-name').textContent = jMsg.msgUserInfo.name;
                document.querySelector('.container-chat--topbar-info-data-status-icon').classList.remove('s-font-color-secondary');
                document.querySelector('.container-chat--topbar-info-data-status-icon').classList.add('s-font-color-green-confirm');
                document.querySelector('.container-chat--topbar-info-data-status-text').textContent = 'Online';
                document.querySelector('.container-chat--topbar-info-data-status-text').classList.remove('s-font-color-secondary');
                document.querySelector('.container-chat--topbar-info-data-status-text').classList.add('s-font-color-primary');
                document.getElementById('s-loader-chat').style.display = 'none';
                document.querySelector('.mdc-text-field--textarea').classList.remove('mdc-text-field--disabled');
                document.querySelector('.mdc-text-field__input').disabled = false;
                document.querySelector('#audioCall').disabled = false;
                document.querySelector('#moreOptionsButton').disabled = false;
                document.querySelector('#videoCall').disabled = false;
                swcms.appendChatMessage(jMsg.msgUserInfo.name + ' Online.', null, 'auto');
                break;
        }
    });
    
    peer.on('stream', (stream) => {
        swcms.setAVStream(stream);
    });
}

// Side menu responsive UI
if (document.querySelector('.container-chat--sidemenu')) {
    let backButtonEl = document.querySelector('.container-chat--topbar-info-back');
    let chatBodyEl = document.querySelector('.container-chat--body');
    let chatFooterEl = document.querySelector('.container-chat--footer');
    let chatTopBarEl = document.querySelector('.container-chat--topbar');
    let sideMenuEl = document.querySelector('.container-chat--sidemenu');

    const initCollapsibleSideMenu = () => {
        backButtonEl.classList.remove('container--hidden');
        if (chatBodyEl.classList.contains('container--hidden')) {
            chatBodyEl.classList.remove('container--hidden');
            chatFooterEl.classList.remove('container--hidden');
            chatTopBarEl.classList.remove('container--hidden');
        }
        sideMenuEl.classList.add('container--hidden');
    }

    const initPermanentSideMenu = () => {
        backButtonEl.classList.add('container--hidden');
        if (chatBodyEl.classList.contains('container--hidden')) {
            chatBodyEl.classList.remove('container--hidden');
            chatFooterEl.classList.remove('container--hidden');
            chatTopBarEl.classList.remove('container--hidden');
        }
        sideMenuEl.classList.remove('container--hidden');
    }

    let sideMenu = window.matchMedia("(max-width: 37.49em)").matches ? initCollapsibleSideMenu() : initPermanentSideMenu();

    // Toggle between permanent sidemenu and collapsible sidemenu at breakpoint 37.5em
    const resizeSideMenuHandler = () => {
        if (window.matchMedia("(max-width: 37.49em)").matches) {
            sideMenu = initCollapsibleSideMenu();
        } else if (window.matchMedia("(min-width: 37.5em)").matches) {
            sideMenu = initPermanentSideMenu();
        }
    }

    window.addEventListener('resize', resizeSideMenuHandler);
}

// Show Contacts List
function showContactsList() {
    let chatBodyEl = document.querySelector('.container-chat--body');
    let chatFooterEl = document.querySelector('.container-chat--footer');
    let chatTopBarEl = document.querySelector('.container-chat--topbar');
    let sideMenuEl = document.querySelector('.container-chat--sidemenu');

    chatBodyEl.classList.add('container--hidden');
    chatFooterEl.classList.add('container--hidden');
    chatTopBarEl.classList.add('container--hidden');
    sideMenuEl.classList.remove('container--hidden');
}
