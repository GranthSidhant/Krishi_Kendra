/**
 * Krishi Kendra - Real-Time Chat, In-Chat Voice Notes & Counter-Offer Negotiation
 */

document.addEventListener('DOMContentLoaded', () => {
  const chatMessages = document.getElementById('chatMessages');
  const chatForm = document.getElementById('chatSendForm');
  const chatInput = document.getElementById('chatInput');
  const threadIdEl = document.getElementById('activeThreadId');

  // Voice recording elements
  const startChatVoiceBtn = document.getElementById('startChatVoiceBtn');
  const voiceRecordingBar = document.getElementById('voiceRecordingBar');
  const recordingTimer = document.getElementById('recordingTimer');
  const cancelVoiceRecordBtn = document.getElementById('cancelVoiceRecordBtn');
  const sendVoiceRecordBtn = document.getElementById('sendVoiceRecordBtn');

  // Offer Modal form
  const inChatOfferForm = document.getElementById('inChatOfferForm');
  const inChatOfferModalEl = document.getElementById('inChatOfferModal');

  if (!chatForm || !threadIdEl) return;

  const threadId = threadIdEl.value;
  let lastMessageId = 0;

  // Auto scroll to bottom
  function scrollToBottom() {
    if (chatMessages) {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  }
  scrollToBottom();

  // Initialize last message ID from existing DOM
  const existing = chatMessages.querySelectorAll('[data-msg-id]');
  if (existing.length > 0) {
    lastMessageId = parseInt(existing[existing.length - 1].getAttribute('data-msg-id')) || 0;
  }

  // 1. Send Text Message
  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (!text) return;

    const formData = new FormData();
    formData.append('message_text', text);
    formData.append('message_type', 'text');

    fetch(`/chat/thread/${threadId}/send`, {
      method: 'POST',
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          chatInput.value = '';
          appendMessageBubble(data.message, true);
          lastMessageId = Math.max(lastMessageId, data.message.id);
          scrollToBottom();
        }
      })
      .catch(err => console.error('Send error:', err));
  });

  // 2. Submit In-Chat Offer / Counter
  if (inChatOfferForm) {
    inChatOfferForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const formData = new FormData(inChatOfferForm);

      fetch(`/chat/thread/${threadId}/send-offer`, {
        method: 'POST',
        body: formData
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            if (inChatOfferModalEl) {
              const modal = bootstrap.Modal.getInstance(inChatOfferModalEl);
              if (modal) modal.hide();
            }
            appendMessageBubble(data.message, true);
            lastMessageId = Math.max(lastMessageId, data.message.id);
            scrollToBottom();
          } else {
            alert(data.error || 'Failed to send offer.');
          }
        })
        .catch(err => console.error('Offer submit error:', err));
    });
  }

  // 3. Voice Recording with MediaRecorder API
  let mediaRecorder = null;
  let audioChunks = [];
  let recordStartTime = 0;
  let recordTimerInterval = null;
  let recordedBlob = null;
  let recordingDurationStr = "0:05";
  let activeStream = null;

  if (startChatVoiceBtn) {
    startChatVoiceBtn.addEventListener('click', async () => {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Audio recording is not supported in this browser environment.');
        return;
      }

      try {
        activeStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioChunks = [];
        recordedBlob = null;

        // Choose best supported MIME type
        let options = undefined;
        if (typeof MediaRecorder.isTypeSupported === 'function') {
          if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
            options = { mimeType: 'audio/webm;codecs=opus' };
          } else if (MediaRecorder.isTypeSupported('audio/webm')) {
            options = { mimeType: 'audio/webm' };
          } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
            options = { mimeType: 'audio/mp4' };
          } else if (MediaRecorder.isTypeSupported('audio/ogg')) {
            options = { mimeType: 'audio/ogg' };
          }
        }

        mediaRecorder = options ? new MediaRecorder(activeStream, options) : new MediaRecorder(activeStream);

        mediaRecorder.ondataavailable = (event) => {
          if (event.data && event.data.size > 0) {
            audioChunks.push(event.data);
          }
        };

        mediaRecorder.onstop = () => {
          const type = (mediaRecorder && mediaRecorder.mimeType) || 'audio/webm';
          recordedBlob = new Blob(audioChunks, { type });
          if (activeStream) {
            activeStream.getTracks().forEach(track => track.stop());
            activeStream = null;
          }
        };

        // Start collecting slices every 250ms
        mediaRecorder.start(250);
        recordStartTime = Date.now();
        showRecordingUI(true);

        recordTimerInterval = setInterval(() => {
          const elapsedSecs = Math.floor((Date.now() - recordStartTime) / 1000);
          const mins = String(Math.floor(elapsedSecs / 60)).padStart(2, '0');
          const secs = String(elapsedSecs % 60).padStart(2, '0');
          if (recordingTimer) recordingTimer.textContent = `${mins}:${secs}`;
          recordingDurationStr = `${mins}:${secs}`;
        }, 1000);

      } catch (err) {
        console.error('Microphone access denied:', err);
        alert('Microphone access is required to record voice notes. Please allow microphone access in your browser settings.');
      }
    });
  }

  function showRecordingUI(isRecording) {
    if (voiceRecordingBar) {
      voiceRecordingBar.style.display = isRecording ? 'flex' : 'none';
    }
    if (chatForm) {
      chatForm.style.display = isRecording ? 'none' : 'flex';
    }
    if (!isRecording && recordTimerInterval) {
      clearInterval(recordTimerInterval);
      if (recordingTimer) recordingTimer.textContent = '00:00';
    }
  }

  if (cancelVoiceRecordBtn) {
    cancelVoiceRecordBtn.addEventListener('click', () => {
      if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        try { mediaRecorder.stop(); } catch(e) {}
      }
      if (activeStream) {
        activeStream.getTracks().forEach(track => track.stop());
        activeStream = null;
      }
      showRecordingUI(false);
      audioChunks = [];
      recordedBlob = null;
    });
  }

  if (sendVoiceRecordBtn) {
    sendVoiceRecordBtn.addEventListener('click', async () => {
      if (!mediaRecorder) return;

      sendVoiceRecordBtn.disabled = true;
      sendVoiceRecordBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Sending...';

      try {
        // Wait for MediaRecorder to stop if still recording
        if (mediaRecorder.state !== 'inactive') {
          await new Promise((resolve) => {
            mediaRecorder.addEventListener('stop', resolve, { once: true });
            mediaRecorder.stop();
          });
        }

        const mime = (mediaRecorder && mediaRecorder.mimeType) || 'audio/webm';
        if (!recordedBlob && audioChunks.length > 0) {
          recordedBlob = new Blob(audioChunks, { type: mime });
        }

        if (recordedBlob && recordedBlob.size > 0) {
          const formData = new FormData();
          const ext = mime.includes('mp4') ? 'mp4' : mime.includes('ogg') ? 'ogg' : 'webm';
          formData.append('audio', recordedBlob, `voice_note.${ext}`);
          formData.append('duration', recordingDurationStr || '0:05');

          const res = await fetch(`/chat/thread/${threadId}/send-voice`, {
            method: 'POST',
            body: formData
          });
          const data = await res.json();
          showRecordingUI(false);
          if (data.success) {
            appendMessageBubble(data.message, true);
            lastMessageId = Math.max(lastMessageId, data.message.id);
            scrollToBottom();
          } else {
            alert(data.error || 'Failed to send voice note.');
          }
        } else {
          showRecordingUI(false);
          alert('Recording was empty. Please speak clearly into your microphone.');
        }
      } catch (err) {
        showRecordingUI(false);
        console.error('Voice send error:', err);
        alert('Failed to send voice note. Please try again.');
      } finally {
        sendVoiceRecordBtn.disabled = false;
        sendVoiceRecordBtn.innerHTML = '<i class="fas fa-paper-plane me-1"></i> Send Voice';
        audioChunks = [];
        recordedBlob = null;
      }
    });
  }

  // 4. Polling for incoming messages every 3.5 seconds
  setInterval(() => {
    fetch(`/chat/thread/${threadId}/poll?since_id=${lastMessageId}`)
      .then(res => res.json())
      .then(data => {
        if (data.messages && data.messages.length > 0) {
          data.messages.forEach(msg => {
            if (!msg.is_me) {
              appendMessageBubble(msg, false);
            }
            lastMessageId = Math.max(lastMessageId, msg.id);
          });
          scrollToBottom();
        }
      })
      .catch(() => {});
  }, 3500);

  function appendMessageBubble(msg, isMe) {
    const bubble = document.createElement('div');
    bubble.className = `msg-bubble ${isMe ? 'msg-sent' : 'msg-received'} mb-3 shadow-sm`;
    bubble.setAttribute('data-msg-id', msg.id);

    const meta = msg.metadata || {};

    if (msg.type === 'phone_shared') {
      bubble.innerHTML = `
        <div class="d-flex align-items-center gap-2 mb-1">
          <span class="badge bg-primary rounded-pill"><i class="fas fa-phone-alt"></i> Contact Shared</span>
        </div>
        <div class="fw-semibold">${escapeHtml(msg.text)}</div>
        <div class="mt-2">
          <a href="tel:${meta.phone || ''}" class="btn btn-sm btn-success px-3"><i class="fas fa-phone-volume me-1"></i> Call ${escapeHtml(meta.phone || '')}</a>
        </div>
        <small class="text-muted d-block text-end mt-1" style="font-size:0.72rem;">${msg.created_at}</small>
      `;
    } else if (msg.type === 'voice_note') {
      bubble.innerHTML = `
        <div class="d-flex align-items-center gap-2 mb-2">
          <i class="fas fa-microphone-alt text-success"></i>
          <span class="fw-bold small">${escapeHtml(meta.sender_name || 'Voice Note')} (${meta.duration || '0:05'})</span>
        </div>
        <audio controls preload="none" class="w-100" style="height: 38px; border-radius: 20px;">
          <source src="${meta.audio_url}" type="audio/webm">
          Your browser does not support audio playback.
        </audio>
        <small class="text-muted d-block text-end mt-1" style="font-size:0.72rem;">${msg.created_at}</small>
      `;
    } else if (msg.type === 'counter_card' || msg.type === 'offer_card') {
      bubble.innerHTML = `
        <div class="border rounded-3 p-3 bg-white text-dark shadow-sm my-1">
          <div class="d-flex justify-content-between align-items-center border-bottom pb-2 mb-2">
            <strong class="text-success"><i class="fas fa-handshake me-1"></i> ${escapeHtml(meta.product_name || 'Produce Offer')}</strong>
            <span class="badge bg-warning text-dark">${escapeHtml(meta.status || 'Countered')}</span>
          </div>
          <div class="row g-2 small mb-2">
            <div class="col-6">
              <span class="text-muted">Offered Price:</span>
              <div class="fw-bold fs-6 text-success">₹${meta.price}/${meta.unit || 'kg'}</div>
            </div>
            <div class="col-6">
              <span class="text-muted">Quantity:</span>
              <div class="fw-bold fs-6">${meta.quantity} ${meta.unit || 'kg'}</div>
            </div>
            <div class="col-12">
              <span class="text-muted">Total:</span>
              <strong class="text-dark">₹${meta.total_amount}</strong>
            </div>
            ${meta.notes ? `<div class="col-12 text-muted fst-italic">"${escapeHtml(meta.notes)}"</div>` : ''}
          </div>
        </div>
        <small class="text-muted d-block text-end mt-1" style="font-size:0.72rem;">${msg.created_at}</small>
      `;
    } else {
      bubble.innerHTML = `
        <div class="msg-text-content" id="msgText_${msg.id}">${escapeHtml(msg.text)}</div>
        <div class="d-flex justify-content-between align-items-center mt-1.5 pt-1 border-top border-light-subtle" style="font-size:0.72rem;">
          <div class="d-flex align-items-center gap-2">
            <button type="button" class="btn btn-xs p-0 text-muted opacity-75 hover-primary" onclick="translateMessage(${msg.id})" title="Translate text">
              <i class="fas fa-language text-primary"></i> <span id="translateBtnLabel_${msg.id}">Translate</span>
            </button>
            <button type="button" class="btn btn-xs p-0 text-muted opacity-75 hover-primary" onclick="speakMessage(${msg.id})" title="Listen to message">
              <i class="fas fa-volume-up text-secondary"></i>
            </button>
          </div>
          <small class="text-muted">${msg.created_at}</small>
        </div>
        <div class="translated-box p-2 mt-1 rounded bg-white text-dark small border d-none" id="translatedBox_${msg.id}">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <span class="badge bg-primary-subtle text-primary" style="font-size:0.68rem;" id="transBadge_${msg.id}">Translated</span>
            <button type="button" class="btn btn-xs p-0 text-muted" onclick="speakTranslated(${msg.id})" title="Listen to translation"><i class="fas fa-volume-up text-primary"></i></button>
          </div>
          <div id="transText_${msg.id}" class="fw-semibold text-dark"></div>
        </div>
      `;
    }

    chatMessages.appendChild(bubble);

    // Auto translate if toggle is active
    const autoToggle = document.getElementById('autoTranslateToggle');
    if (autoToggle && autoToggle.checked && !isMe) {
      setTimeout(() => translateMessage(msg.id), 250);
    }
  }

  function escapeHtml(string) {
    if (!string) return '';
    const div = document.createElement('div');
    div.innerText = string;
    return div.innerHTML;
  }

  // 5. Global In-Chat Translation & Speech Handlers
  window.translateMessage = function(msgId) {
    const textEl = document.getElementById(`msgText_${msgId}`);
    if (!textEl) return;
    const text = textEl.innerText.trim();
    if (!text) return;

    const langSelect = document.getElementById('chatTargetLangSelect');
    const targetLang = langSelect ? langSelect.value : 'hi';
    const btnLabel = document.getElementById(`translateBtnLabel_${msgId}`);
    const box = document.getElementById(`translatedBox_${msgId}`);
    const resultText = document.getElementById(`transText_${msgId}`);
    const badge = document.getElementById(`transBadge_${msgId}`);

    if (btnLabel) btnLabel.textContent = 'Translating...';

    fetch('/api/chat/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text, target_lang: targetLang })
    })
      .then(res => res.json())
      .then(data => {
        if (btnLabel) btnLabel.textContent = 'Translate';
        if (data.success && box && resultText) {
          resultText.textContent = data.translated_text;
          if (badge) badge.textContent = `Translated to ${data.target_lang_name || targetLang.toUpperCase()}`;
          box.classList.remove('d-none');
          scrollToBottom();
        }
      })
      .catch(err => {
        if (btnLabel) btnLabel.textContent = 'Translate';
        console.error('Translate error:', err);
      });
  };

  window.speakMessage = function(msgId) {
    const textEl = document.getElementById(`msgText_${msgId}`);
    if (!textEl || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(textEl.innerText.trim());
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  };

  window.speakTranslated = function(msgId) {
    const transEl = document.getElementById(`transText_${msgId}`);
    if (!transEl || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();

    const langSelect = document.getElementById('chatTargetLangSelect');
    const targetLang = langSelect ? langSelect.value : 'hi';

    const utterance = new SpeechSynthesisUtterance(transEl.innerText.trim());
    utterance.lang = targetLang === 'hi' ? 'hi-IN' : (targetLang === 'mr' ? 'mr-IN' : (targetLang === 'ta' ? 'ta-IN' : (targetLang === 'te' ? 'te-IN' : 'en-IN')));
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  };

  // Auto-translate toggle event
  const autoTranslateToggle = document.getElementById('autoTranslateToggle');
  if (autoTranslateToggle) {
    autoTranslateToggle.addEventListener('change', (e) => {
      if (e.target.checked) {
        // Translate all received messages in DOM
        const receivedBubbles = chatMessages.querySelectorAll('.msg-received[data-msg-id]');
        receivedBubbles.forEach(b => {
          const id = b.getAttribute('data-msg-id');
          if (id) translateMessage(parseInt(id));
        });
      }
    });
  }
});

