import {defineStore} from 'pinia'

// Хранилище состояния Pinia
export const usePiniaStore = defineStore(
  'pinia',
  {
    state: () => ({
      loader: true,
      products: []
    }),
    getters: {
      // Получить параметр отображения загрушки
      getLoader: (state) => state.loader,
      // Получить данные по товарам
      getProduces: (state) => state.products
    },
    actions: {
      // Изменить отображение заглушки
      changeLoader(onlyHide = false) {
        if (onlyHide) {
          this.loader = false
          return
        }
        this.loader = !(this.loader)
      },
      // Установить полученные данные о товарах
      setProducts(data) {
        this.products = data
      }
    }
  }
)
