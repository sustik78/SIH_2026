import React, { createContext, useContext, useState, useEffect } from 'react';

const AccessibilityContext = createContext(null);

export const AccessibilityProvider = ({ children }) => {
  const [seniorMode, setSeniorMode] = useState(() => localStorage.getItem('praman_senior_mode') === 'true');
  const [highContrast, setHighContrast] = useState(() => localStorage.getItem('praman_high_contrast') === 'true');
  const [audioGuidance, setAudioGuidance] = useState(() => localStorage.getItem('praman_audio_guidance') === 'true');

  useEffect(() => {
    localStorage.setItem('praman_senior_mode', seniorMode);
    if (seniorMode) {
      document.body.classList.add('senior-mode');
    } else {
      document.body.classList.remove('senior-mode');
    }
  }, [seniorMode]);

  useEffect(() => {
    localStorage.setItem('praman_high_contrast', highContrast);
    if (highContrast) {
      document.body.classList.add('high-contrast');
    } else {
      document.body.classList.remove('high-contrast');
    }
  }, [highContrast]);

  const speakText = (text) => {
    if (!audioGuidance || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
  };

  return (
    <AccessibilityContext.Provider
      value={{
        seniorMode,
        setSeniorMode,
        highContrast,
        setHighContrast,
        audioGuidance,
        setAudioGuidance,
        speakText
      }}
    >
      {children}
    </AccessibilityContext.Provider>
  );
};

export const useAccessibility = () => useContext(AccessibilityContext);
