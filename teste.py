class request():
    def __init__(self):
        self.metodo='GET'
        self.GET=''
        self.POST=None
        print('objeto criado')

    def change_metodo(self, arg):
        self.metodo=arg

    def get_POST(self, args):
        resposta={}
        for i in args:
            
            resposta[i]=args[i]
        self.POST=resposta



request=request()
print(request.metodo)
request.change_metodo('POST')
print(request.metodo)
request.get_POST({'username': 'salarini', 'password': '123456'})
print(request.POST)
print(request.GET)
print(request.POST['username'])



