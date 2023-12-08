import streamlit as st

def solveur_transport(grid, offre, demande):
    INF = 10**3
    n = len(grid)
    m = len(grid[0])
    ans = 0
    affectations = []

    def trouver_diff(grid):
        diff_ligne = []
        diff_colonne = []
        for i in range(len(grid)):
            arr = grid[i][:]
            arr.sort()
            diff_ligne.append(arr[1] - arr[0])

        col = 0
        while col < len(grid[0]):
            arr = []
            for i in range(len(grid)):
                arr.append(grid[i][col])
            arr.sort()
            col += 1
            diff_colonne.append(arr[1] - arr[0])

        return diff_ligne, diff_colonne

    while max(offre) != 0 or max(demande) != 0:
        ligne, colonne = trouver_diff(grid)
        maxi1 = max(ligne)
        maxi2 = max(colonne)

        if maxi1 >= maxi2:
            for ind, val in enumerate(ligne):
                if val == maxi1:
                    mini1 = min(grid[ind])
                    for ind2, val2 in enumerate(grid[ind]):
                        if val2 == mini1:
                            mini2 = min(offre[ind], demande[ind2])
                            ans += mini2 * mini1
                            affectations.append((ind, ind2, mini2))
                            offre[ind] -= mini2
                            demande[ind2] -= mini2

                            if demande[ind2] == 0:
                                for r in range(n):
                                    grid[r][ind2] = INF
                            else:
                                grid[ind] = [INF for i in range(m)]
                            break
                    break
        else:
            for ind, val in enumerate(colonne):
                if val == maxi2:
                    mini1 = INF
                    for j in range(n):
                        mini1 = min(mini1, grid[j][ind])

                    for ind2 in range(n):
                        val2 = grid[ind2][ind]
                        if val2 == mini1:
                            mini2 = min(offre[ind2], demande[ind])
                            ans += mini2 * mini1
                            affectations.append((ind2, ind, mini2))
                            offre[ind2] -= mini2
                            demande[ind] -= mini2

                            if demande[ind] == 0:
                                for r in range(n):
                                    grid[r][ind] = INF
                            else:
                                grid[ind2] = [INF for i in range(m)]
                            break
                    break

    return ans, affectations

def main():
    st.title("Solveur de Problème de Transport avec l'aaproximation de Vogel ")

    st.sidebar.header("Entrer les données:")
    n = st.sidebar.slider("Lignes (n):", 1, 10, 2)
    m = st.sidebar.slider("Colonnes (m):", 1, 10, 2)

    grid = []
    st.sidebar.subheader("Entrer la Matrice des Coûts:")
    for i in range(n):
        row = []
        for j in range(m):
            element = st.sidebar.number_input(f"Élément à ({i+1}, {j+1}):", min_value=0, value=1)
            row.append(element)
        grid.append(row)

    offre = []
    st.sidebar.subheader("Entrer le Vecteur d'Offre:")
    for i in range(n):
        offre.append(st.sidebar.number_input(f"Offre à ({i+1}):", min_value=0, value=1))

    demande = []
    st.sidebar.subheader("Entrer le Vecteur de Demande:")
    for j in range(m):
        demande.append(st.sidebar.number_input(f"Demande à ({j+1}):", min_value=0, value=1))

    if st.sidebar.button("Résoudre"):
        st.header("Résultats:")
        resultat, affectations = solveur_transport(grid, offre, demande)
        st.write(f"La solution de base réalisable est {resultat}")
        st.write("Affectations:")
        for affectation in affectations:
            st.write(f"Ligne {affectation[0] + 1}, Colonne {affectation[1] + 1}: {affectation[2]} unités")

if __name__ == "__main__":
    main()
