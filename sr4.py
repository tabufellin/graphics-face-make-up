from render import Render

gl = Render(2048, 2048)										
gl.load('./tarea1/Bowl.obj', (0, 0, 0), (16, 16, 16))
gl.display('bowl.bmp')
