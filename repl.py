import pygments
from lark import UnexpectedInput
from prompt_toolkit import Application
from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, Window, VSplit, BufferControl, FormattedTextControl, HSplit, ScrollablePane
from prompt_toolkit.styles import Style
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.widgets import TextArea, Frame, VerticalLine, HorizontalLine

from interpreter import LambdaInterpreter
from pygment_lexer import LambdaLexer


class REPL:
    kb = KeyBindings()

    def __init__(self, filenames=None):
        help_text = "exit program: c-q\nprint steps: c-s\nnormal evaluate: c-d"
        self.step = False

        self.interpreter = LambdaInterpreter(filenames)

        self.text_area = TextArea(
            prompt=" > ",
            height=1,
            lexer=PygmentsLexer(LambdaLexer),
            multiline=False,
            accept_handler=self.enter_text,
        )
        self.formatted_text = BufferControl(lexer=PygmentsLexer(LambdaLexer), focusable=False)

        self.root = HSplit([
            VSplit([
                Window(content=self.formatted_text, wrap_lines=True),
                VerticalLine(),
                Window(content=FormattedTextControl(text=help_text), width=20)
            ]),
            HorizontalLine(),
            self.text_area
        ])

    def enter_text(self, buffer):
        self.formatted_text.buffer.insert_text("\n > " + buffer.text)

        try:
            if self.step:
                for output in self.interpreter.eval_steps(buffer.text):
                    self.formatted_text.buffer.insert_text("\n" + str(output))
            else:
                output = self.interpreter.eval(buffer.text)
                self.formatted_text.buffer.insert_text("\n" + str(output))

        except UnexpectedInput as e:
            output = e.get_context(buffer.text)
            self.formatted_text.buffer.insert_text("\nError")

    def __pt_container__(self):
        return self.root


if __name__ == '__main__':
    style = Style.from_dict({
        'pygments.keyword': '#0CDF75 bold',
        'pygments.literal': '#DF2E0C italic',
    })

    repl = REPL("declarations.lambda")

    layout = Layout(repl)

    kb = KeyBindings()

    @kb.add('c-q')
    def exit_(event):
        event.app.exit()


    @kb.add('c-s')
    def step_(event):
        repl.step = True


    @kb.add('c-d')
    def nostep_(event):
        repl.step = False

    app = Application(layout=layout, full_screen=True, style=style, key_bindings=kb)
    app.run()  # You won't be able to Exit this app
