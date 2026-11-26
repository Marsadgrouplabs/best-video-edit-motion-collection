<p align="center"><b>English</b> · <a href="SECURITY.ar.md">العربية</a></p>

# Security in Best Video Edit & Motion Collection

## Who is the publisher?

[Marsad Labs](https://labs.marsadgroup.co) is the product arm of Marsad Group, a UK-registered marketing agency. [About us](https://labs.marsadgroup.co/about-us/) · [Privacy policy](https://labs.marsadgroup.co/privacy-policy/)

## What does this skill do with your data?

| Question | Answer |
|---|---|
| **What does it read?** | Only the videos and files you give it. |
| **Where does the video go?** | Editing runs on your computer. If you ask for generated scenes or images, that request goes to the service you chose, such as fal.ai or Google. |
| **Does it need API keys?** | Not for regular editing. Generation keys are optional and stay with you. |
| **Heads-up** | The editing studio opens a link on your local network while it runs, so close it when you finish. |

## Scan result

- **Tool:** SkillSpector, an automated scan that does not send the files to any external model.
- **Automated risk score:** 100/100, rated critical.
- **Alerts:** 3 critical, 16 high, 124 medium, 13 low.
- **Main cause of the alerts after manual review:** The scripts send your key only to the service you chose, and the delete commands clear temporary folders inside the working folder.
- **New in v2.0.0:** the installers read the local `components.json` to copy only the parts you pick. They make no network calls and keep a backup of any older copy.
- **New in v1.1.0:** the bundled real-sfx (Clipwing) was scanned on its own (100/100, critical). Every critical and high alert was reviewed by hand: patterns in tests and normal script options, no outbound data and no remote code. Its network listening option is disabled in this build.
- **Review limits:** we reviewed the critical and high alerts by hand. Scanning reduces risk but is not a full guarantee, so check the permissions before using any skill.

## Verify the file

Every release on the Releases page includes a `SHA256SUMS.txt` file. Compare the hash of your download with the one listed there:

```powershell
Get-FileHash .\best-video-edit-motion-collection.zip -Algorithm SHA256
```

## Found a security problem?

Send it to `Labs@marsadgroup.co` and please do not disclose it publicly until it is fixed.
