import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._choiceLocation = None

    def handleCreaGrafo(self, e):
        provider = self._view._ddProvider.value
        if provider is None:
            print("Seleziona provider.")
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Seleziona un provider."))
            self._view.update_page()
            return

        soglia = self._view._txtInDistanza.value
        if soglia == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Distanza non inserita."))
            self._view.update_page()
            return

        try:
            sogliaFloat = float(soglia)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione! Soglia inserita non numerica!"))
            self._view._txt_result.controls.clear()
            return

        self._model.buildGraph(provider, sogliaFloat)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato correttamente. "
                                                       f"Il grafo ha {nNodes} nodi e {nEdges} archi."))
        self.fillDDTarget()
        self._view.update_page()

    def handleAnalizzaGrafo(self, e):
        nNodes, nEdges = self._model.getGraphDetails()
        if nNodes == 0 and nEdges == 0:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione! Grafo vuoto."))
            self._view.update_page()
            return

        lista = self._model.getNodesMostVicini()

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Nodi con più vicini:"))
        for l in lista:
            self._view._txt_result.controls.append(ft.Text(f"{l[0]} -- {l[1]}"))
        self._view.update_page()

    def handleCalcolaPercorso(self, e):
        target = self._choiceLocation
        substring = self._view._txtInString.value
        if substring == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione! Stringa non inserita."))
            self._view.update_page()
            return

        path, source = self._model.getCammino(target, substring)

        if path == []:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Cammino tra {source} e {target} non trovato."))
            self._view.update_page()
            return

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Cammino tra {source} e {target} trovato."))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))
            self._view.update_page()

    def fillDDProvider(self):
        providers = self._model.getAllProviders()
        providers.sort()

        # Modo 1:
        # for p in providers:
        #     self._view._ddProvider.options.append(ft.dropdown.Option(p))
        # self._view.update_page()

        # Modo 2:
        providersDD = map(lambda x: ft.dropdown.Option(x), providers)
        self._view._ddProvider.options.extend(providersDD)
        self._view.update_page()

    def fillDDTarget(self):
        locations = self._model.getAllLocations()

        locationsDD = map(lambda x: ft.dropdown.Option(data=x, text=x.Location,
                                                       on_click=self.readChoiceLocation), locations)
        self._view._ddTarget.options.extend(locationsDD)

    def readChoiceLocation(self, e):
        if e.control.data is None:
            self._choiceLocation = None
        else:
            self._choiceLocation = e.control.data
