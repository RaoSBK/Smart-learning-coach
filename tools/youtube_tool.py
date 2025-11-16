import yt_dlp
import requests

class YouTubeTranscriptTool:

    @staticmethod
    def get_metadata(url):
        """
        Extracts metadata: title, description, duration, thumbnail.
        """
        try:
            ydl_opts = {"quiet": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                metadata = {
                    "title": info.get("title"),
                    "description": info.get("description"),
                    "duration": info.get("duration"),
                    "thumbnail": info.get("thumbnail"),
                    "view_count": info.get("view_count"),
                }
                return metadata

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_transcript(url: str) -> str:
        """
        Fetch YouTube subtitles (auto or manual).
        """
        try:
            ydl_opts = {
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitlesformat": "vtt",
                "skip_download": True,
                "quiet": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                subs = info.get("subtitles") or info.get("automatic_captions")

                if not subs:
                    return None  # Transcript missing

                lang = "en" if "en" in subs else list(subs.keys())[0]

                sub_url = subs[lang][0]["url"]
                vtt_data = requests.get(sub_url).text

                cleaned = []
                for line in vtt_data.splitlines():
                    if "-->" not in line and line.strip() and "WEBVTT" not in line:
                        cleaned.append(line)

                return " ".join(cleaned)

        except Exception:
            return None
