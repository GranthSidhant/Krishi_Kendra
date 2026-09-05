/**
 * Krishi Kendra - Multilingual AI Voice & Text Copilot (Krishi Mitra)
 * Features Web Speech API Recognition + Synthesis + Intelligent Query Processor
 */

document.addEventListener('DOMContentLoaded', () => {
  const micFab = document.getElementById('voiceAssistantFab');
  const voiceModalEl = document.getElementById('voiceAssistantModal');
  const startRecBtn = document.getElementById('startVoiceRecordingBtn');
  const voiceStatusText = document.getElementById('voiceStatusText');
  const voiceResponseText = document.getElementById('voiceResponseText');
  const voiceActionContainer = document.getElementById('voiceActionContainer');
  const voiceTextForm = document.getElementById('voiceTextQueryForm');
  const voiceTextInput = document.getElementById('voiceTextInput');
  const quickChips = document.querySelectorAll('.ai-quick-chip');

  if (!micFab) return;

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  let recognition = null;
  let isListening = false;

  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    // Detect language or default to Hindi / Indian English
    const currentLang = document.documentElement.lang || 'hi-IN';
    recognition.lang = currentLang === 'hi' ? 'hi-IN' : (currentLang === 'mr' ? 'mr-IN' : 'en-IN');

    recognition.onstart = () => {
      isListening = true;
      if (startRecBtn) {
        startRecBtn.classList.remove('btn-outline-success');
        startRecBtn.classList.add('btn-danger', 'pulse-animation');
        startRecBtn.innerHTML = '<i class="fas fa-stop fa-2x"></i>';
      }
      if (micFab) micFab.classList.add('listening');
      if (voiceStatusText) voiceStatusText.textContent = "Listening... Speak now in Hindi or English";
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      if (voiceStatusText) voiceStatusText.innerHTML = `Heard: <strong class="text-primary">"${transcript}"</strong>`;
      processAIQuery(transcript);
    };

    recognition.onerror = (event) => {
      console.warn('Speech recognition error:', event.error);
      stopListeningUI();
      if (voiceStatusText) voiceStatusText.textContent = "Could not hear audio clearly. You can also type below!";
    };

    recognition.onend = () => {
      stopListeningUI();
    };
  }

  function stopListeningUI() {
    isListening = false;
    if (startRecBtn) {
      startRecBtn.classList.remove('btn-danger', 'pulse-animation');
      startRecBtn.classList.add('btn-outline-success');
      startRecBtn.innerHTML = '<i class="fas fa-microphone-alt fa-2x"></i>';
    }
    if (micFab) micFab.classList.remove('listening');
  }

  function toggleVoiceListening() {
    if (!recognition) {
      if (voiceStatusText) {
        voiceStatusText.textContent = "Microphone voice input is not supported on this browser. Please type your query below!";
      }
      return;
    }

    if (isListening) {
      recognition.stop();
    } else {
      try {
        recognition.start();
      } catch (err) {
        console.warn(err);
      }
    }
  }

  // Floating Action Button Click
  micFab.addEventListener('click', () => {
    if (voiceModalEl) {
      const modal = bootstrap.Modal.getOrCreateInstance(voiceModalEl);
      modal.show();
    }
    toggleVoiceListening();
  });

  // Modal Mic Button Click
  if (startRecBtn) {
    startRecBtn.addEventListener('click', toggleVoiceListening);
  }

  // Quick chips click
  quickChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const query = chip.dataset.query || chip.textContent.trim();
      if (voiceStatusText) voiceStatusText.innerHTML = `Query: <strong class="text-primary">"${query}"</strong>`;
      processAIQuery(query);
    });
  });

  // Text Query Form Submission
  if (voiceTextForm && voiceTextInput) {
    voiceTextForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const query = voiceTextInput.value.trim();
      if (!query) return;
      if (voiceStatusText) voiceStatusText.innerHTML = `Query: <strong class="text-primary">"${query}"</strong>`;
      processAIQuery(query);
      voiceTextInput.value = '';
    });
  }

  function processAIQuery(queryText) {
    if (voiceResponseText) {
      voiceResponseText.innerHTML = '<span class="spinner-border spinner-border-sm me-2 text-success"></span> Consulting Krishi Mitra AI...';
    }
    if (voiceActionContainer) {
      voiceActionContainer.style.display = 'none';
      voiceActionContainer.innerHTML = '';
    }

    fetch('/api/voice-query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: queryText })
    })
      .then(res => res.json())
      .then(data => {
        if (voiceResponseText) {
          voiceResponseText.textContent = data.response_text;
        }
        speakReply(data.response_text);

        if (data.action_url && voiceActionContainer) {
          voiceActionContainer.innerHTML = `
            <a href="${data.action_url}" class="btn btn-sm btn-success fw-bold">
              <i class="fas fa-external-link-alt me-1"></i> ${data.action_label || 'Go to Page'}
            </a>
          `;
          voiceActionContainer.style.display = 'block';
        }
      })
      .catch(err => {
        console.error('AI query error:', err);
        if (voiceResponseText) {
          voiceResponseText.textContent = "Sorry, unable to connect to Krishi Mitra service right now. Please try again.";
        }
      });
  }

  function speakReply(text) {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.95;
      utterance.pitch = 1.0;
      // Use Hindi voice if available
      const voices = window.speechSynthesis.getVoices();
      const hiVoice = voices.find(v => v.lang.includes('hi') || v.name.includes('Hindi'));
      if (hiVoice) utterance.voice = hiVoice;
      window.speechSynthesis.speak(utterance);
    }
  }
});
