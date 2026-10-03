I need you to finish my Telegram automation bot.

GOAL:
I have 2 Telegram groups. The bot must receive an audio/voice message and automatically send the same audio as a proper Telegram voice message to BOTH target groups.

IMPORTANT:
- Do NOT send anything to the groups until the bot is fully configured and I explicitly test it.
- Keep the bot stopped while configuration is incomplete.
- Do not require ElevenLabs API for the basic test if I provide an existing audio sample.
- If ElevenLabs conversion is already implemented, keep it, but make the system work with a local/uploaded audio sample first.
- Do not expose Telegram bot tokens or API keys in source code. Use environment variables / Replit Secrets.

FUNCTIONALITY:

1. Admin sends an audio file or voice message to the bot.
2. Bot downloads the audio.
3. If necessary, convert it to Telegram-compatible voice-message format:
   - OGG
   - Opus codec
   - mono
4. Send the converted audio as a Telegram voice message to BOTH configured target groups.
5. Send a confirmation to the admin after both messages are successfully sent.
6. If sending to one group fails, clearly report which group failed and why.
7. Do not send duplicate messages accidentally.
8. Add useful logging so I can see:
   - audio received
   - conversion started/completed
   - group 1 send result
   - group 2 send result
   - errors

CONFIGURATION:

Use environment variables / Replit Secrets:

TELEGRAM_BOT_TOKEN
TARGET_GROUP_1
TARGET_GROUP_2

Optional if ElevenLabs is used:

ELEVENLABS_API_KEY

Do not hard-code any secrets.

TARGET GROUPS:
I will provide the two Telegram group IDs/usernames through Replit Secrets or configuration. Do not invent them.

ADMIN SECURITY:
Only allow my Telegram user ID(s) to trigger the bot. Create:

ADMIN_USER_ID

If ADMIN_USER_ID is not configured, do not send messages to the target groups.

TELEGRAM REQUIREMENTS:
- The bot must be added to both target groups.
- Verify that the bot has permission to send voice messages.
- If a group ID is invalid or the bot is not a member/admin, give a clear error instead of crashing.

AUDIO:
If the incoming file is already a Telegram voice message, forward/re-send it as a voice message.
If it is an MP3/WAV/M4A/etc., convert it to OGG/Opus using ffmpeg if ffmpeg is available.
Do not send it as a normal document or audio file; use Telegram's voice-message type.

TEST MODE:
Add a TEST_MODE environment variable.

When:
TEST_MODE=true

the bot should NOT send anything to the real groups. Instead, log exactly what it WOULD send and to which group.

When:
TEST_MODE=false

it may send to the configured target groups.

IMPORTANT FOR MY CURRENT SITUATION:
Replit currently says that my free monthly quota has been reached. Do not pretend that the bot is running if Replit cannot execute it.
First make the code/configuration ready.
Then tell me exactly what I need to do in Replit to run a test.

Also create a simple /status command that reports:
- bot configuration status
- whether TARGET_GROUP_1 is configured
- whether TARGET_GROUP_2 is configured
- whether TEST_MODE is enabled
- whether required dependencies are installed

Do NOT display secret values.

Before making any changes that could send a real message to my Telegram groups, show me the final configuration and ask me to confirm.

Finally, give me a short TEST CHECKLIST:
1. Add bot to group 1.
2. Add bot to group 2.
3. Give required permissions.
4. Add Telegram bot token to Replit Secrets.
5. Add both group IDs.
6. Add my admin Telegram ID.
7. Set TEST_MODE=true.
8. Run the bot.
9. Test with an audio message.
10. If everything works, change TEST_MODE=false and test again.

Please inspect the existing project first and modify the existing implementation rather than unnecessarily rebuilding the entire project.
