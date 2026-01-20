# Voice Options for Warmer Sound

## Current Voice
- **Provider**: 11labs
- **Voice ID**: `21m00Tcm4TlvDq8ikWAM`

## Finding a Warmer Voice

### Option 1: Browse 11labs Voices (Recommended)

1. Go to https://elevenlabs.io
2. Log in to your account
3. Navigate to "Voices" section
4. Listen to different voices and look for:
   - Warm, friendly tones
   - Natural, conversational sound
   - Female voices often sound warmer for customer service calls
5. Copy the Voice ID of the one you like
6. Update `voiceId` in `vapi_config.json`

### Option 2: Try These Popular Warm Voice IDs

Here are some commonly used warm voices (you'll need to verify these work with your 11labs account):

**Female Voices (typically warmer for customer service):**
- `EXAVITQu4vr4xnSDxMaL` - Bella (warm, friendly)
- `ThT5KcBeYPX3keUQqHPh` - Dorothy (warm, professional)
- `VR6AewLTigWG4xSOukaG` - Arnold (if you want male)

**Note**: Voice IDs may vary by account. Best to browse in your dashboard.

### Option 3: Adjust Current Voice Settings

You can also make the current voice warmer by adjusting settings:

```json
"voice": {
  "provider": "11labs",
  "voiceId": "21m00Tcm4TlvDq8ikWAM",
  "stability": 0.4,        // Lower = more variation (more natural)
  "similarityBoost": 0.8,  // Higher = more like original (warmer)
  "style": 0.2,            // Slight style boost for warmth
  "useSpeakerBoost": true
}
```

### Option 4: Try Different Providers

You can also try other voice providers that might have warmer options:

**Azure TTS:**
```json
"voice": {
  "provider": "azure",
  "voiceId": "en-US-JennyNeural"  // Warm, friendly female voice
}
```

**Google:**
```json
"voice": {
  "provider": "google",
  "voiceId": "en-US-Neural2-F"  // Natural female voice
}
```

## Testing Different Voices

1. Update the `voiceId` in `vapi_config.json`
2. Run a test call: `python3 test_call.py 224-245-4540`
3. Listen to how it sounds
4. Adjust or try another voice

## Tips for Warmer Sound

- **Female voices** often sound warmer for customer service
- **Lower stability** (0.3-0.5) = more natural variation
- **Higher similarityBoost** (0.7-0.9) = maintains warmth
- **Style boost** (0.1-0.3) = adds character
