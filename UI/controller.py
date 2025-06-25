import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        if self._view.ddyear.value is None:
            self._view.create_alert("Selezionare anno!")
            return
        anno = int(self._view.ddyear.value)
        if self._view.ddstate.value is None or self._view.ddstate.value == "":
            self._view.create_alert("Selezionare stato!")
            return
        stato = self._view.ddstate.value

        self._view.txt_result1.controls.clear()
        self._model.buildGraph(anno, stato)
        self._view.txt_result1.controls.append(ft.Text("Grafo creato correttamente"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model.getNumEdges()}"))

        self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha: {self._model.getNumCompConessa()} componenti connesse"))
        connessa = self._model.getLargestConnessa()
        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande "
                                                       f"è costituita da {len(connessa)} nodi:"))
        for c in connessa:
            self._view.txt_result1.controls.append(ft.Text(c))

        self._view.update_page()

    def handle_path(self, e):
        pass

    def fillDDAnno(self):
        for a in self._model.getAnni():
            self._view.ddyear.options.append(ft.dropdown.Option(a))
        self._view.update_page()

    def fillDDState(self, anno):
        anno = int(self._view.ddyear.value)
        self._view.ddstate.options.clear()
        for s in self._model.getState(anno):
            self._view.ddstate.options.append(ft.dropdown.Option(s))
        self._view.update_page()