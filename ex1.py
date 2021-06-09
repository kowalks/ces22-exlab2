# CES-22: Programação Orientada a Objetos
# Aluno: Guilherme Kowalczuk (COMP-23)

# Descrição da Atividade:

# Considerando o exemplo do CoffeShop com Padrão de Projeto Decorator. Crie um
# exemplo que construa Pizzas. Ao invés de itens para um café, usar ingredientes de
# pizza. O Diagrama de Classes deve ser elaborado.

class Ingrediente:  # Clase Componente
    cost = 0.0

    def get_description(self):
        return self.__class__.__name__

    def get_total_cost(self):
        return self.__class__.cost


class MassaBase(Ingrediente):  # Classe ComponenteConcreto
    cost = 5.0  # A massa é mais cara, para adicionar um custo inicial grande para cada pizza


class Decorator(Ingrediente):  # Classe Decorator
    def __init__(self, ingrediente):
        self.component = ingrediente

    def get_total_cost(self):
        return self.component.get_total_cost() + self.__class__.cost

    def get_description(self):
        return self.component.get_description() + ', ' + self.__class__.__name__


class MassaDeTomate(Decorator):  # Classe DecoratorConcretoA
    cost = 2.0


class Pepperoni(Decorator):  # Classe DecoratorConcretoB
    cost = 1.0


class Mozzarella(Decorator):  # Classe DecoratorConcretoC
    cost = 1.0


class Tomate(Decorator):  # Classe DecoratorConcretoD
    cost = 1.0


class Manjericao(Decorator):  # Classe DecoratorConcretoE
    cost = 0.5


class Frango(Decorator):  # Classe DecoratorConcretoF
    cost = 1.5


class Catupiry(Decorator):  # Classe DecoratorConcretoG
    cost = 0.7


class Pizza:  # Classe Pizza, só para encapsular o nome da pizza junto com os ingredientes
    def __init__(self, nome, pizza):
        self.nome = nome
        self.pizza = pizza

    def __str__(self):
        return self.nome + ': ' + self.pizza.get_description() + ' ($' + str(self.pizza.get_total_cost()) + ')'


# Criamos três pizzas com sabores diferentes
frango_com_catupity = Pizza('Frango com Catupiry', Catupiry(Frango(MassaDeTomate(MassaBase()))))
pepperoni = Pizza('Pepperoni', Pepperoni(Mozzarella(MassaDeTomate(MassaBase()))))
margherita = Pizza('Margherita', Manjericao(Tomate(Mozzarella(MassaDeTomate(MassaBase())))))

# Para cada pizza, imprimimos resultado da agregação de decoradores e o preço respectivo
print(frango_com_catupity)
print(pepperoni)
print(margherita)

# Observação: diferente do exemplo dado em aula, não implementei explicitamente o método construtor __init__
# para as classes que herdam de Decorator porque, em Python, se não há explícitamente o método construtor,
# ele sempre chama o da superclasse correspondente. Em aula esse método é chamado explicitamente fazendo
# Decorator.__init__(), mas tal comando não é necessário.
