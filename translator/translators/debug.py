from translator.core.plugin import (
    Translator,
    TranslatorResult,
    OcrResult,
    PluginTextArgument,
    PluginArgument,
)
import tkinter as tk
from tkinter import scrolledtext

class DebugTranslator(Translator):
    """Writes the specified text"""

    def __init__(self, text="") -> None:
        super().__init__()
        self.to_write = text
        self.editor = None
        self.edited_text = None

    async def translate(self, batch: list[OcrResult]):
        print("translate Method Called ")
        if not self.editor:
            self.create_editor(batch)

        self.editor.mainloop()

        if self.edited_text is not None:
            individual_texts = [line.split(':', 1)[1] for line in self.edited_text.split('\n')]

            self.editor = None
            self.edited_text = None
            return [TranslatorResult(idv_text) for idv_text in individual_texts]
        else:
            return [TranslatorResult("ocr_result.text") for ocr_result in batch]

    def create_editor(self, batch: list[OcrResult]):
        root = tk.Tk()
        root.title("Text Editor")

        text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)

        initial_text = "\n".join(f"dialog{i + 1}:{ocr_result.text}" for i, ocr_result in enumerate(batch))
        text_area.insert(tk.INSERT, initial_text)

        def on_closing():
            self.edited_text = text_area.get("1.0", "end-1c")
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        self.editor = root

    @staticmethod
    def get_name() -> str:
        return "Custom Text"

    @staticmethod
    def get_arguments() -> list[PluginArgument]:
        return [
            PluginTextArgument(
                id="text", name="Debug Text", description="What to write"
            )
        ]