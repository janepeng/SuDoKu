import tornado.ioloop
import tornado.web
import os.path
import sudoku

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")

class SolveHandler(tornado.web.RequestHandler):
    def post(self):
        sudoku_input = ''
        for i in range(0, 9):
            line = ''
            for j in range(0, 9):
                val = self.get_argument(str(i) + str(j), '')
                if val == '':
                    val = '0'
                line += val + ' '
            sudoku_input += line[:-1] + '\n'
        board = sudoku.solve_sudoku(sudoku_input)
        message = ' '.join(str(item) for innerlist in board for item in innerlist)
        self.write(message)

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/submit", SolveHandler)
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static")
    )
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
