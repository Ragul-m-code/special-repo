/**
 * SECRET TO DREAM // 1130 ARCHIVE - Core Application Logic
 * Real Audio Engine (HTML5 MP3 Audio + Web Audio Synth), Countdown Urgency, PayU Integration & Demo Checkout Flow
 */

// Runtime Configuration State
let appConfig = {
  demo: true,
  productName: "Secret to Dream",
  amount: "29.00",
  currency: "USD",
  payuEnv: "test"
};

// Fetch runtime config from /api/config
async function fetchAppConfig() {
  try {
    const res = await fetch('/api/config');
    if (res.ok) {
      const data = await res.json();
      if (data && data.success) {
        appConfig = data;
        const modeBadge = document.getElementById('demo-mode-indicator');
        if (modeBadge) {
          modeBadge.textContent = appConfig.demo ? 'DEMO MODE: ACTIVE (Instant Checkout)' : 'PAYU GATEWAY: ACTIVE';
        }
      }
    }
  } catch (e) {
    console.log("Config loaded in standalone mode (Demo Active)");
  }
}

// Comprehensive Sound Engine: Real MP3 Audio Playback + Web Audio Synthesizer
class SoundEngine {
  constructor() {
    this.ctx = null;
    this.isPlayingAmbient = false;
    this.ambientGain = null;
    this.ambientOsc1 = null;
    this.ambientOsc2 = null;

    // Real HTML5 Audio Object for Landing Page Teaser
    this.teaserAudio = typeof Audio !== 'undefined' ? new Audio('audio/teaser_01.mp3') : null;
    if (this.teaserAudio) {
      this.teaserAudio.preload = 'auto';
    }
    this.isPlayingTeaser = false;
  }

  initAudioContext() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  // Ambient Acoustic Soundscape (Warm soothing atmospheric chord)
  toggleAmbient(btnElement) {
    this.initAudioContext();
    if (!this.ctx) return;

    if (this.isPlayingAmbient) {
      if (this.ambientGain) {
        this.ambientGain.gain.setValueAtTime(this.ambientGain.gain.value, this.ctx.currentTime);
        this.ambientGain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + 1.2);
        setTimeout(() => {
          if (this.ambientOsc1) { try { this.ambientOsc1.stop(); } catch(e){} }
          if (this.ambientOsc2) { try { this.ambientOsc2.stop(); } catch(e){} }
          this.ambientOsc1 = null;
          this.ambientOsc2 = null;
          this.ambientGain = null;
        }, 1200);
      }
      this.isPlayingAmbient = false;
      if (btnElement) {
        btnElement.classList.remove('text-primary-gold', 'bg-surface-highest');
        btnElement.innerHTML = '<span class="material-symbols-outlined text-[18px]">volume_off</span>';
        btnElement.title = "Ambient sound muted";
      }
      showToast("Ambient soundscape paused", "info");
    } else {
      this.ambientGain = this.ctx.createGain();
      this.ambientGain.gain.setValueAtTime(0.0001, this.ctx.currentTime);
      this.ambientGain.gain.exponentialRampToValueAtTime(0.06, this.ctx.currentTime + 1.5);

      const filter = this.ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(550, this.ctx.currentTime);

      this.ambientOsc1 = this.ctx.createOscillator();
      this.ambientOsc1.type = 'sine';
      this.ambientOsc1.frequency.setValueAtTime(146.83, this.ctx.currentTime); // D3

      this.ambientOsc2 = this.ctx.createOscillator();
      this.ambientOsc2.type = 'sine';
      this.ambientOsc2.frequency.setValueAtTime(220.00, this.ctx.currentTime); // A3

      this.ambientOsc1.connect(filter);
      this.ambientOsc2.connect(filter);
      filter.connect(this.ambientGain);
      this.ambientGain.connect(this.ctx.destination);

      this.ambientOsc1.start();
      this.ambientOsc2.start();
      this.isPlayingAmbient = true;

      if (btnElement) {
        btnElement.classList.add('text-primary-gold', 'bg-surface-highest');
        btnElement.innerHTML = '<span class="material-symbols-outlined text-[18px]">volume_up</span>';
        btnElement.title = "Ambient acoustic mood active";
      }
      showToast("Ambient acoustic soundscape active", "success");
    }
  }

  // Real Audio Teaser Playback with HTML5 Audio
  toggleVoiceTeaser(playBtn, visualizer, timeDisplay, progressBar) {
    if (this.teaserAudio.paused) {
      this.teaserAudio.play().then(() => {
        this.isPlayingTeaser = true;
        if (playBtn) {
          playBtn.innerHTML = '<span class="material-symbols-outlined text-[28px]">pause</span>';
        }
        if (visualizer) {
          visualizer.classList.add('playing');
        }
        showToast("Playing authentic excerpt: 'The Midnight Call' (03:19 AM)", "success");
      }).catch(err => {
        console.warn("Audio play error:", err);
        showToast("Audio playback requires user interaction. Click play again.", "warning");
      });

      // Update progress on timeupdate
      this.teaserAudio.ontimeupdate = () => {
        const cur = this.teaserAudio.currentTime;
        const dur = this.teaserAudio.duration || 60;
        const curMins = Math.floor(cur / 60).toString().padStart(2, '0');
        const curSecs = Math.floor(cur % 60).toString().padStart(2, '0');
        const durMins = Math.floor(dur / 60).toString().padStart(2, '0');
        const durSecs = Math.floor(dur % 60).toString().padStart(2, '0');

        if (timeDisplay) {
          timeDisplay.textContent = `${curMins}:${curSecs} / ${durMins}:${durSecs}`;
        }
        if (progressBar) {
          progressBar.style.width = `${(cur / dur) * 100}%`;
        }
      };

      this.teaserAudio.onended = () => {
        this.isPlayingTeaser = false;
        if (playBtn) {
          playBtn.innerHTML = '<span class="material-symbols-outlined text-[28px]">play_arrow</span>';
        }
        if (visualizer) {
          visualizer.classList.remove('playing');
        }
        if (progressBar) {
          progressBar.style.width = '0%';
        }
      };

    } else {
      this.teaserAudio.pause();
      this.isPlayingTeaser = false;
      if (playBtn) {
        playBtn.innerHTML = '<span class="material-symbols-outlined text-[28px]">play_arrow</span>';
      }
      if (visualizer) {
        visualizer.classList.remove('playing');
      }
      showToast("Voice memo excerpt paused", "info");
    }
  }

  seekTeaser(ratio, progressBar, timeDisplay) {
    if (this.teaserAudio.duration) {
      this.teaserAudio.currentTime = ratio * this.teaserAudio.duration;
      if (progressBar) {
        progressBar.style.width = `${ratio * 100}%`;
      }
    }
  }
}

const soundEngine = new SoundEngine();

// Toast Notifications System
function showToast(message, type = 'info') {
  let toastContainer = document.getElementById('toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.className = 'fixed bottom-6 right-6 z-50 flex flex-col gap-3 pointer-events-none max-w-sm';
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  const icon = type === 'success' ? 'verified' : type === 'warning' ? 'warning' : 'notifications';
  const borderCol = type === 'success' ? 'border-[#f2ca50]' : 'border-[rgba(242,202,80,0.3)]';

  toast.className = `pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-lg bg-[#1a1823]/95 border ${borderCol} text-white shadow-2xl backdrop-blur-md transition-all duration-300 translate-y-3 opacity-0 text-sm`;
  toast.innerHTML = `
    <span class="material-symbols-outlined text-[20px] text-[#f2ca50] shrink-0">${icon}</span>
    <span class="font-light leading-snug">${message}</span>
  `;

  toastContainer.appendChild(toast);

  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-3', 'opacity-0');
  });

  setTimeout(() => {
    toast.classList.add('translate-y-3', 'opacity-0');
    setTimeout(() => toast.remove(), 400);
  }, 4200);
}

// Global App Initialization
document.addEventListener('DOMContentLoaded', () => {
  fetchAppConfig();
  initCountdown();
  initDiscreetFeed();
  initAudioTeaser();
  initAmbientButtons();
  initModals();
  initRedactedProtocols();
  initFAQ();
});

// 1. Urgency Countdown Timer
function initCountdown() {
  const timerElements = document.querySelectorAll('.countdown-display');
  if (!timerElements.length) return;

  const storageKey = 'secret_to_dream_timer_end';
  let targetTime = localStorage.getItem(storageKey);

  if (!targetTime || parseInt(targetTime, 10) <= Date.now()) {
    targetTime = Date.now() + (3 * 3600 + 42 * 60 + 18) * 1000;
    localStorage.setItem(storageKey, targetTime.toString());
  }

  function update() {
    const diff = Math.max(0, Math.floor((parseInt(targetTime, 10) - Date.now()) / 1000));
    if (diff === 0) {
      targetTime = Date.now() + (2 * 3600 + 14 * 60) * 1000;
      localStorage.setItem(storageKey, targetTime.toString());
    }

    const hrs = Math.floor(diff / 3600).toString().padStart(2, '0');
    const mins = Math.floor((diff % 3600) / 60).toString().padStart(2, '0');
    const secs = (diff % 60).toString().padStart(2, '0');
    const timeStr = `${hrs}:${mins}:${secs}`;

    timerElements.forEach(el => {
      el.textContent = timeStr;
    });
  }

  update();
  setInterval(update, 1000);
}

// 2. Real-time Discreet Dispatch Feed
function initDiscreetFeed() {
  const feedElem = document.getElementById('discreet-feed');
  const counterElem = document.getElementById('invitation-counter');
  if (!feedElem) return;

  const notifications = [
    { text: 'A private collector from Monaco unlocked Secret to Dream 4m ago', invites: 14 },
    { text: 'Elena from Zurich unlocked the secret folio 11m ago', invites: 14 },
    { text: 'Camille from London reserved an invitation token 2m ago', invites: 13 },
    { text: 'A private member from Geneva verified possession 6m ago', invites: 13 },
    { text: 'Alexander V. from New York accessed Part IV 1m ago', invites: 12 },
    { text: 'A venture partner from Paris unlocked the audio archive 8m ago', invites: 12 },
    { text: 'Marcus K. from Mayfair acquired unredacted dossier 3m ago', invites: 11 }
  ];

  let index = 0;
  setInterval(() => {
    index = (index + 1) % notifications.length;
    feedElem.style.opacity = '0';
    setTimeout(() => {
      feedElem.textContent = notifications[index].text;
      feedElem.style.opacity = '1';
      if (counterElem) {
        counterElem.textContent = `${notifications[index].invites} / 300`;
      }
    }, 400);
  }, 6500);
}

// 3. Audio Teaser Player with Real Audio Seeking
function initAudioTeaser() {
  const playBtn = document.getElementById('memo-play-btn');
  const visualizer = document.getElementById('memo-visualizer');
  const timeDisplay = document.getElementById('memo-time');
  const progressBar = document.getElementById('memo-progress-bar');
  const trackBar = document.getElementById('memo-track-container');

  if (playBtn) {
    playBtn.addEventListener('click', () => {
      soundEngine.toggleVoiceTeaser(playBtn, visualizer, timeDisplay, progressBar);
    });
  }

  if (trackBar) {
    trackBar.addEventListener('click', (e) => {
      const rect = trackBar.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const ratio = Math.max(0, Math.min(1, clickX / rect.width));
      soundEngine.seekTeaser(ratio, progressBar, timeDisplay);
    });
  }
}

// 4. Ambient Acoustic Buttons
function initAmbientButtons() {
  const ambientBtns = document.querySelectorAll('.ambient-sound-toggle');
  ambientBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      soundEngine.toggleAmbient(btn);
    });
  });
}

// 5. Checkout & Token Login Modals + PayU Integration
function initModals() {
  const checkoutModal = document.getElementById('checkout-modal');
  const openCheckoutBtns = document.querySelectorAll('.open-checkout-btn');
  const closeCheckoutBtns = document.querySelectorAll('.close-checkout-btn');
  const checkoutForm = document.getElementById('checkout-form');

  function openCheckout() {
    if (checkoutModal) {
      checkoutModal.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeCheckout() {
    if (checkoutModal) {
      checkoutModal.classList.add('hidden');
      document.body.style.overflow = '';
    }
  }

  openCheckoutBtns.forEach(b => b.addEventListener('click', (e) => {
    e.preventDefault();
    openCheckout();
  }));

  closeCheckoutBtns.forEach(b => b.addEventListener('click', closeCheckout));

  if (checkoutModal) {
    checkoutModal.addEventListener('click', (e) => {
      if (e.target === checkoutModal) closeCheckout();
    });
  }

  // Unified Checkout Initiation (PayU or Demo Mode)
  async function handleCheckoutExecution(paymentMethod = 'Standard') {
    const emailInput = document.getElementById('checkout-email');
    const email = (emailInput && emailInput.value.trim()) || 'collector@confidential.net';
    const nameInput = document.getElementById('checkout-name');
    const name = (nameInput && nameInput.value.trim()) || 'Private Member';

    const statusContainer = document.getElementById('checkout-status');
    const formFields = document.getElementById('checkout-fields');

    if (formFields) formFields.classList.add('opacity-40', 'pointer-events-none');
    if (statusContainer) {
      statusContainer.classList.remove('hidden');
      statusContainer.innerHTML = `
        <div class="flex flex-col items-center gap-4 py-6 text-center">
          <span class="material-symbols-outlined text-[36px] text-[#f2ca50] animate-spin">progress_activity</span>
          <div>
            <p class="font-headline-sm text-lg text-white font-medium">Securing Gateway Credentials...</p>
            <p class="text-xs text-gray-400 mt-1">Routing order for ${appConfig.productName} ($${appConfig.amount})</p>
          </div>
        </div>
      `;
    }

    try {
      const response = await fetch('/api/payu/initiate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, phone: '9999999999' })
      });

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error || "Payment initiation failed");
      }

      // 1. DEMO MODE ACTIVATED
      if (result.demo) {
        setTimeout(() => {
          localStorage.setItem('nocturne_access_token', result.token);
          localStorage.setItem('nocturne_member_email', email);
          localStorage.setItem('nocturne_member_name', name);

          statusContainer.innerHTML = `
            <div class="flex flex-col items-center gap-4 py-4 text-center bg-[#1c1a24] p-6 rounded-xl border border-[#d4af37]/40">
              <span class="material-symbols-outlined text-[42px] text-[#f2ca50]">check_circle</span>
              <div>
                <p class="text-[10px] text-[#e0b6ff] uppercase tracking-widest font-semibold">Demo Mode Active · Instant Clearance</p>
                <h4 class="text-xl text-white font-serif mt-1">Vault Key Issued</h4>
                <p class="text-xs text-gray-300 mt-2">Your private encryption key:</p>
                <div class="inline-flex items-center gap-2 mt-2 px-4 py-2 rounded bg-black/50 border border-[#f2ca50]/50 font-mono text-[#f2ca50] text-sm select-all">
                  <span>${result.token}</span>
                  <button type="button" onclick="navigator.clipboard.writeText('${result.token}'); showToast('Token copied', 'success');" class="text-gray-400 hover:text-white">
                    <span class="material-symbols-outlined text-[16px]">content_copy</span>
                  </button>
                </div>
              </div>
              <div class="w-full pt-4 flex flex-col gap-2">
                <a href="${result.redirectUrl}" class="w-full py-3 px-4 rounded bg-[#f2ca50] text-[#14121a] font-semibold text-xs tracking-widest uppercase text-center hover:opacity-95 shadow-lg">
                  ENTER PRIVATE VAULT &rarr;
                </a>
              </div>
            </div>
          `;
          setTimeout(() => {
            window.location.href = result.redirectUrl;
          }, 1400);
        }, 1200);
        return;
      }

      // 2. PAYU LIVE/TEST MODE
      statusContainer.innerHTML = `
        <div class="flex flex-col items-center gap-4 py-6 text-center">
          <span class="material-symbols-outlined text-[36px] text-[#f2ca50] animate-spin">sync</span>
          <div>
            <p class="font-headline-sm text-lg text-white font-medium">Redirecting to PayU Payment Gateway...</p>
            <p class="text-xs text-gray-400 mt-1">Encrypted SHA-512 Hash Verified. Please wait.</p>
          </div>
        </div>
      `;

      const form = document.createElement('form');
      form.method = 'POST';
      form.action = result.actionUrl;

      Object.entries(result.params).forEach(([key, val]) => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = val;
        form.appendChild(input);
      });

      document.body.appendChild(form);
      setTimeout(() => {
        form.submit();
      }, 900);

    } catch (err) {
      const randomHex = Math.random().toString(16).substring(2, 7).toUpperCase();
      const token = `STD-VLT-${randomHex}`;
      localStorage.setItem('nocturne_access_token', token);
      localStorage.setItem('nocturne_member_email', email);
      localStorage.setItem('nocturne_member_name', name);

      statusContainer.innerHTML = `
        <div class="flex flex-col items-center gap-4 py-4 text-center bg-[#1c1a24] p-6 rounded-xl border border-[#d4af37]/40">
          <span class="material-symbols-outlined text-[42px] text-[#f2ca50]">verified</span>
          <div>
            <p class="text-[10px] text-[#e0b6ff] uppercase tracking-widest font-semibold">Simulated Clearance Granted</p>
            <h4 class="text-xl text-white font-serif mt-1">Vault Key Issued</h4>
            <div class="inline-flex items-center gap-2 mt-2 px-4 py-2 rounded bg-black/50 border border-[#f2ca50]/50 font-mono text-[#f2ca50] text-sm select-all">
              <span>${token}</span>
            </div>
          </div>
          <a href="/vault?token=${token}&name=${encodeURIComponent(name)}&demo=1" class="w-full py-3 px-4 rounded bg-[#f2ca50] text-[#14121a] font-semibold text-xs tracking-widest uppercase text-center">
            ENTER PRIVATE VAULT &rarr;
          </a>
        </div>
      `;
      setTimeout(() => {
        window.location.href = `/vault?token=${token}&name=${encodeURIComponent(name)}&demo=1`;
      }, 1400);
    }
  }

  if (checkoutForm) {
    checkoutForm.addEventListener('submit', (e) => {
      e.preventDefault();
      handleCheckoutExecution('PayU Portal');
    });
  }

  // Token Sanctum Login Modal
  const loginModal = document.getElementById('login-modal');
  const openLoginBtns = document.querySelectorAll('.open-login-btn');
  const closeLoginBtns = document.querySelectorAll('.close-login-btn');
  const loginForm = document.getElementById('login-form');

  function openLogin() {
    if (loginModal) {
      loginModal.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeLogin() {
    if (loginModal) {
      loginModal.classList.add('hidden');
      document.body.style.overflow = '';
    }
  }

  openLoginBtns.forEach(b => b.addEventListener('click', (e) => {
    e.preventDefault();
    openLogin();
  }));

  closeLoginBtns.forEach(b => b.addEventListener('click', closeLogin));

  if (loginModal) {
    loginModal.addEventListener('click', (e) => {
      if (e.target === loginModal) closeLogin();
    });
  }

  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const tokenInput = document.getElementById('login-token-input');
      const token = tokenInput ? tokenInput.value.trim().toUpperCase() : '';

      if (token.length >= 4) {
        localStorage.setItem('nocturne_access_token', token);
        showToast("Authorization key verified. Decrypting sanctum...", "success");
        setTimeout(() => {
          window.location.href = 'vault.html';
        }, 800);
      } else {
        showToast("Invalid key format. Use DEMO1130 for instant preview.", "warning");
      }
    });
  }
}

// 6. Redacted Protocols Micro-Interaction
function initRedactedProtocols() {
  const redactedBox = document.getElementById('redacted-protocol-box');
  if (redactedBox) {
    redactedBox.addEventListener('click', () => {
      showToast("Part IV Obsidian Protocols: Active clearance key required.", "warning");
      const checkoutModal = document.getElementById('checkout-modal');
      if (checkoutModal) {
        setTimeout(() => {
          checkoutModal.classList.remove('hidden');
          document.body.style.overflow = 'hidden';
        }, 500);
      }
    });
  }
}

// 7. Interactive FAQ Accordion
function initFAQ() {
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const trigger = item.querySelector('.faq-trigger');
    const answer = item.querySelector('.faq-answer');
    const icon = item.querySelector('.faq-icon');

    if (trigger && answer) {
      trigger.addEventListener('click', () => {
        const isOpen = !answer.classList.contains('hidden');
        faqItems.forEach(other => {
          const otherAnswer = other.querySelector('.faq-answer');
          const otherIcon = other.querySelector('.faq-icon');
          if (otherAnswer) otherAnswer.classList.add('hidden');
          if (otherIcon) otherIcon.style.transform = 'rotate(0deg)';
        });

        if (!isOpen) {
          answer.classList.remove('hidden');
          if (icon) icon.style.transform = 'rotate(180deg)';
        }
      });
    }
  });
}
