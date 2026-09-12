/**
 * Krishi Kendra - Kisan Saarthi (किसान सारथी)
 * Conversational Multilingual AI Voice Copilot powered by Google Gemini AI
 * Features Multi-turn Chat Memory + Dynamic Multilingual Voice Synthesis + Context Actions
 */

document.addEventListener('DOMContentLoaded', () => {
  const micFab = document.getElementById('voiceAssistantFab');
  const voiceModalEl = document.getElementById('voiceAssistantModal');
  const startRecBtn = document.getElementById('startVoiceRecordingBtn');
  const micBtnIcon = document.getElementById('micBtnIcon');
  const voiceStatusText = document.getElementById('voiceStatusText');
  const voicePulseDot = document.getElementById('voicePulseDot');
  const audioWaveVisualizer = document.getElementById('audioWaveVisualizer');
  const chatStream = document.getElementById('kisanChatStream');
  const voiceTextForm = document.getElementById('voiceTextQueryForm');
  const voiceTextInput = document.getElementById('voiceTextInput');
  const quickChips = document.querySelectorAll('.ai-quick-chip');
  const toggleMuteBtn = document.getElementById('toggleVoiceMuteBtn');
  const voiceMuteIcon = document.getElementById('voiceMuteIcon');
  const clearHistoryBtn = document.getElementById('clearChatHistoryBtn');

  if (!micFab || !voiceModalEl) return;

  // State
  let isListening = false;
  let isMuted = false;
  let conversationHistory = [];
  let availableVoices = [];

  // Determine current active interface language
  function getActiveLang() {
    return document.documentElement.lang || 'en';
  }

  // 1. Dynamic Multilingual Voice Engine (Routes audio to native voice per language)
  function initAvailableVoices() {
    if (!('speechSynthesis' in window)) return;
    availableVoices = window.speechSynthesis.getVoices() || [];
  }

  if ('speechSynthesis' in window) {
    window.speechSynthesis.onvoiceschanged = initAvailableVoices;
    initAvailableVoices();
  }

  function getBestVoiceForText(text, targetLang) {
    if (!availableVoices || availableVoices.length === 0) {
      initAvailableVoices();
    }
    if (!availableVoices || availableVoices.length === 0) return null;

    const hasDevanagari = /[\u0900-\u097F]/.test(text);
    const hasTamil = /[\u0B80-\u0BFF]/.test(text);
    const hasTelugu = /[\u0C00-\u0C7F]/.test(text);

    if (hasDevanagari || targetLang === 'hi' || targetLang === 'mr') {
      return availableVoices.find(v => v.lang === 'hi-IN' || v.lang.startsWith('hi') || v.name.includes('Hindi') || v.name.includes('हिन्दी'))
          || availableVoices.find(v => v.lang === 'mr-IN' || v.lang.startsWith('mr'))
          || availableVoices.find(v => v.lang.includes('IN'))
          || availableVoices[0];
    }

    if (hasTamil || targetLang === 'ta') {
      return availableVoices.find(v => v.lang === 'ta-IN' || v.lang.startsWith('ta'))
          || availableVoices.find(v => v.lang.includes('IN'))
          || availableVoices[0];
    }

    if (hasTelugu || targetLang === 'te') {
      return availableVoices.find(v => v.lang === 'te-IN' || v.lang.startsWith('te'))
          || availableVoices.find(v => v.lang.includes('IN'))
          || availableVoices[0];
    }

    // Default to natural Indian English or standard English
    return availableVoices.find(v => v.lang === 'en-IN' || v.name.includes('India') || v.name.includes('Indian'))
        || availableVoices.find(v => v.lang === 'en-US' || v.lang === 'en-GB' || v.lang.startsWith('en'))
        || availableVoices[0];
  }

  // 2. Speech Recognition Setup
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  let recognition = null;

  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    // Detect language or default to current page language
    const currentLang = getActiveLang();
    recognition.lang = currentLang === 'hi' ? 'hi-IN' : (currentLang === 'mr' ? 'mr-IN' : (currentLang === 'ta' ? 'ta-IN' : (currentLang === 'te' ? 'te-IN' : 'en-IN')));

    recognition.onstart = () => {
      isListening = true;
      const langNotice = currentLang === 'hi' ? "सुन रहा हूँ... बोलिए (हिंदी या अंग्रेजी)" : (currentLang === 'mr' ? "ऐकत आहे... बोला (मराठी किंवा इंग्रजी)" : "Listening... Speak in English or your native language");
      updateStatusUI('recording', langNotice);
      if (micBtnIcon) {
        micBtnIcon.className = 'fas fa-stop text-white';
        startRecBtn.classList.remove('btn-success');
        startRecBtn.classList.add('btn-danger', 'pulse-animation');
      }
      if (micFab) micFab.classList.add('listening');
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      if (transcript && transcript.trim()) {
        sendUserQuery(transcript.trim());
      }
    };

    recognition.onerror = (event) => {
      console.warn('Speech recognition notice:', event.error);
      stopListeningUI();
      updateStatusUI('idle', "Could not capture audio clearly. Please try again or type below.");
    };

    recognition.onend = () => {
      stopListeningUI();
    };
  }

  function stopListeningUI() {
    isListening = false;
    if (micBtnIcon) {
      micBtnIcon.className = 'fas fa-microphone fa-lg text-white';
      startRecBtn.classList.remove('btn-danger', 'pulse-animation');
      startRecBtn.classList.add('btn-success');
    }
    if (micFab) micFab.classList.remove('listening');
    if (!window.speechSynthesis || !window.speechSynthesis.speaking) {
      const currentLang = getActiveLang();
      const prompt = currentLang === 'hi' ? "माइक दबाकर बोलें या नीचे लिखें" : (currentLang === 'mr' ? "माइक दाबा किंवा खाली लिहा" : "Press mic to speak or type in English/Hindi");
      updateStatusUI('idle', prompt);
    }
  }

  function toggleVoiceListening() {
    if (!recognition) {
      updateStatusUI('idle', "Microphone voice input is not supported on this browser. Please type below.");
      if (voiceTextInput) voiceTextInput.focus();
      return;
    }

    if (isListening) {
      recognition.stop();
    } else {
      // Cancel any ongoing speech
      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
      try {
        const currentLang = getActiveLang();
        recognition.lang = currentLang === 'hi' ? 'hi-IN' : (currentLang === 'mr' ? 'mr-IN' : 'en-IN');
        recognition.start();
      } catch (err) {
        console.warn(err);
      }
    }
  }

  function updateStatusUI(state, message) {
    if (voiceStatusText) voiceStatusText.textContent = message;
    if (voicePulseDot) {
      voicePulseDot.className = 'status-indicator-dot ' + (state === 'recording' ? 'recording' : (state === 'speaking' ? 'speaking' : ''));
    }
    if (audioWaveVisualizer) {
      audioWaveVisualizer.style.display = (state === 'recording' || state === 'speaking') ? 'flex' : 'none';
    }
  }

  // 3. Floating Action Button & Modal Controls
  micFab.addEventListener('click', () => {
    const modal = bootstrap.Modal.getOrCreateInstance(voiceModalEl);
    modal.show();
    setTimeout(() => toggleVoiceListening(), 400);
  });

  if (startRecBtn) {
    startRecBtn.addEventListener('click', toggleVoiceListening);
  }

  // Mute / Unmute voice output
  if (toggleMuteBtn) {
    toggleMuteBtn.addEventListener('click', () => {
      isMuted = !isMuted;
      if (isMuted) {
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        voiceMuteIcon.className = 'fas fa-volume-mute';
        toggleMuteBtn.classList.add('btn-warning');
        toggleMuteBtn.classList.remove('btn-outline-light');
      } else {
        voiceMuteIcon.className = 'fas fa-volume-up';
        toggleMuteBtn.classList.remove('btn-warning');
        toggleMuteBtn.classList.add('btn-outline-light');
      }
    });
  }

  // Reset conversation history
  if (clearHistoryBtn) {
    clearHistoryBtn.addEventListener('click', () => {
      conversationHistory = [];
      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
      const currentLang = getActiveLang();
      const resetMsg = currentLang === 'hi' ? "बातचीत रीसेट हो गई है। आप नए सवाल पूछ सकते हैं!" : (currentLang === 'mr' ? "संभाषण रीसेट झाले आहे. नवीन प्रश्न विचारा!" : "Conversation reset. You can ask a new question!");
      if (chatStream) {
        chatStream.innerHTML = `
          <div class="chat-msg chat-msg-ai mb-3 d-flex gap-2">
            <div class="chat-avatar bg-success text-white rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 36px; height: 36px;">
              <i class="fas fa-robot text-xs"></i>
            </div>
            <div class="chat-bubble bg-white p-3 rounded-3 shadow-xs border" style="max-width: 85%;">
              <div class="fw-bold text-success small mb-1"><i class="fas fa-brain me-1"></i> Kisan Saarthi</div>
              <div class="chat-text text-dark">${resetMsg}</div>
            </div>
          </div>
        `;
      }
      updateStatusUI('idle', "Conversation reset. Press mic to start.");
    });
  }

  // Quick Chips Query
  quickChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const query = chip.dataset.query || chip.textContent.trim();
      sendUserQuery(query);
    });
  });

  // Text Form Submission
  if (voiceTextForm && voiceTextInput) {
    voiceTextForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const query = voiceTextInput.value.trim();
      if (!query) return;
      voiceTextInput.value = '';
      sendUserQuery(query);
    });
  }

  // 4. Send Query to Gemini AI with Context & Language
  function sendUserQuery(userText) {
    stopListeningUI();
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();

    // Append User Message to UI
    appendUserBubble(userText);

    // Append AI Loading Bubble
    const aiBubbleId = 'ai-loading-' + Date.now();
    appendLoadingAIBubble(aiBubbleId);
    updateStatusUI('speaking', "Consulting agricultural intelligence...");

    const currentLang = getActiveLang();

    // Send payload with active language
    fetch('/api/voice-query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: userText,
        history: conversationHistory,
        language: currentLang
      })
    })
      .then(res => res.json())
      .then(data => {
        // Replace loading bubble with actual AI response
        replaceWithAIResponse(aiBubbleId, data);
        
        // Save to multi-turn conversation memory
        conversationHistory.push({ role: 'user', content: userText });
        conversationHistory.push({ role: 'model', content: data.response_text || '' });

        // Speak response out loud in its matching language
        if (!isMuted && data.response_text) {
          speakReply(data.response_text, data.language || currentLang);
        } else {
          updateStatusUI('idle', "Press mic to speak or type in English/Hindi");
        }
      })
      .catch(err => {
        console.error('AI Voice Error:', err);
        replaceWithAIError(aiBubbleId);
        updateStatusUI('idle', "Press mic to speak or type in English/Hindi");
      });
  }

  // 5. Chat UI Helpers
  function appendUserBubble(text) {
    if (!chatStream) return;
    const msgEl = document.createElement('div');
    msgEl.className = 'chat-msg chat-msg-user mb-3 d-flex gap-2';
    msgEl.innerHTML = `
      <div class="chat-bubble p-3 rounded-3 shadow-xs" style="max-width: 85%;">
        <div class="fw-semibold text-primary small mb-0.5"><i class="fas fa-user-circle me-1"></i> You:</div>
        <div class="chat-text text-dark">${escapeHtml(text)}</div>
      </div>
      <div class="chat-avatar bg-primary text-white rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 36px; height: 36px;">
        <i class="fas fa-microphone-lines text-xs"></i>
      </div>
    `;
    chatStream.appendChild(msgEl);
    scrollToBottom();
  }

  function appendLoadingAIBubble(id) {
    if (!chatStream) return;
    const msgEl = document.createElement('div');
    msgEl.className = 'chat-msg chat-msg-ai mb-3 d-flex gap-2';
    msgEl.id = id;
    msgEl.innerHTML = `
      <div class="chat-avatar bg-success text-white rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 36px; height: 36px;">
        <i class="fas fa-seedling text-xs"></i>
      </div>
      <div class="chat-bubble bg-white p-3 rounded-3 shadow-xs border" style="max-width: 85%;">
        <div class="fw-bold text-success small mb-1"><i class="fas fa-brain me-1"></i> Kisan Saarthi</div>
        <div class="d-flex align-items-center gap-2 text-muted small">
          <span class="spinner-border spinner-border-sm text-success"></span>
          <span>Consulting Live Mandi & Intelligence...</span>
        </div>
      </div>
    `;
    chatStream.appendChild(msgEl);
    scrollToBottom();
  }

  function replaceWithAIResponse(id, data) {
    const loadingEl = document.getElementById(id);
    if (!loadingEl) return;

    let actionBtnHtml = '';
    if (data.action_url) {
      actionBtnHtml = `
        <div class="mt-2.5">
          <a href="${data.action_url}" class="btn btn-xs btn-success rounded-pill fw-bold shadow-xs">
            <i class="fas fa-arrow-up-right-from-square me-1"></i> ${escapeHtml(data.action_label || 'View Details')}
          </a>
        </div>
      `;
    }

    loadingEl.innerHTML = `
      <div class="chat-avatar bg-success text-white rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 36px; height: 36px;">
        <i class="fas fa-seedling text-xs"></i>
      </div>
      <div class="chat-bubble bg-white p-3 rounded-3 shadow-xs border" style="max-width: 85%;">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <div class="fw-bold text-success small"><i class="fas fa-brain me-1"></i> Kisan Saarthi</div>
          ${data.is_ai ? '<span class="badge bg-light text-success border text-xs px-2 py-0.5 rounded-pill">Gemini AI</span>' : ''}
        </div>
        <div class="chat-text text-dark">${escapeHtml(data.response_text || '')}</div>
        ${actionBtnHtml}
      </div>
    `;
    scrollToBottom();
  }

  function replaceWithAIError(id) {
    const loadingEl = document.getElementById(id);
    if (!loadingEl) return;
    const currentLang = getActiveLang();
    const errorMsg = currentLang === 'hi' ? "क्षमा करें, सर्वर से संपर्क नहीं हो सका। कृपया दोबारा प्रयास करें।" : (currentLang === 'mr' ? "क्षमस्व, सर्व्हरशी संपर्क होऊ शकला नाही. कृपया पुन्हा प्रयत्न करा." : "Sorry, could not connect to server. Please try again.");
    loadingEl.innerHTML = `
      <div class="chat-avatar bg-secondary text-white rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 36px; height: 36px;">
        <i class="fas fa-exclamation text-xs"></i>
      </div>
      <div class="chat-bubble bg-white p-3 rounded-3 shadow-xs border text-danger small" style="max-width: 85%;">
        ${errorMsg}
      </div>
    `;
    scrollToBottom();
  }

  function scrollToBottom() {
    if (chatStream) {
      chatStream.scrollTop = chatStream.scrollHeight;
    }
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // 6. Dynamic Multilingual Voice Synthesis
  function speakReply(text, targetLang) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();

    const voice = getBestVoiceForText(text, targetLang);
    const utterance = new SpeechSynthesisUtterance(text);
    
    if (voice) {
      utterance.voice = voice;
      utterance.lang = voice.lang;
    } else {
      const hasDevanagari = /[\u0900-\u097F]/.test(text);
      utterance.lang = hasDevanagari ? 'hi-IN' : 'en-IN';
    }
    
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    utterance.onstart = () => {
      updateStatusUI('speaking', "Speaking answer out loud...");
    };

    utterance.onend = () => {
      const currentLang = getActiveLang();
      const prompt = currentLang === 'hi' ? "माइक दबाकर बोलें या नीचे लिखें" : (currentLang === 'mr' ? "माइक दाबा किंवा खाली लिहा" : "Press mic to speak or type in English/Hindi");
      updateStatusUI('idle', prompt);
    };

    utterance.onerror = () => {
      updateStatusUI('idle', "Press mic to speak or type in English/Hindi");
    };

    window.speechSynthesis.speak(utterance);
  }
});
