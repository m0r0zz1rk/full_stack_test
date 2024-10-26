<template>
  <v-data-table
    :headers="headers"
    :items="piniaStore.products"
    :sort-by="[{ key: 'created_at', order: 'asc' }]"
    :loading="piniaStore.loader"
  >
    <template v-slot:top>
      <v-toolbar
        flat
      >
        <v-toolbar-title>Товары</v-toolbar-title>
        <v-divider
          class="mx-4"
          inset
          vertical
        ></v-divider>
        <v-spacer></v-spacer>
        <v-dialog
          v-model="dialog"
          max-width="500px"
        >
          <template v-slot:activator="{ props }">
            <v-btn
              class="mb-2"
              color="primary"
              dark
              v-bind="props"
              @click="setProduct(null); productId = -1"
              :loading="piniaStore.loader"
            >
              Новый товар
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="text-h5">
                {{ productId === -1 ? 'Новый товар' : 'Редактирование товара' }}
              </span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <template
                    v-for="header in headers"
                  >
                    <v-col
                      v-if="!(['created_at', 'actions'].includes(header.key))"
                      cols="12"
                      md="6"
                      sm="6"
                    >
                      <v-text-field
                        v-if="['category', 'name', 'description'].includes(header.key)"
                        :label="header.title"
                        :loading="piniaStore.loader"
                        v-model="selectedProduct[header.key]"
                      />
                      <v-number-input
                        v-if="['price', 'count'].includes(header.key)"
                        :label="header.title"
                        :loading="piniaStore.loader"
                        v-model="selectedProduct[header.key]"
                      />
                    </v-col>
                  </template>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="blue-darken-1"
                variant="text"
                @click="dialog=!dialog"
                :loading="piniaStore.loader"
              >
                Отмена
              </v-btn>
              <v-btn
                color="blue-darken-1"
                variant="text"
                @click="productSave"
                :loading="piniaStore.loader"
              >
                {{ productId === -1 ? 'Добавить' : 'Изменить' }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon
        class="me-2"
        size="small"
        :loading="piniaStore.loader"
        @click="setProduct(item); productId = item.id; dialog=!dialog"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        size="small"
        :loading="piniaStore.loader"
        @click="productDelete(item.id)"
      >
        mdi-delete
      </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn
        color="primary"
        @click="initialize"
      >
        Reset
      </v-btn>
    </template>
  </v-data-table>
</template>

<script>

// Основная страница
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import {usePiniaStore} from "@/modules/pinia/store";

export default {
  name: 'MainPage',
  setup() {
    const piniaStore = usePiniaStore()
    return { piniaStore }
  },
  data() {
    return {
      // ID редактируемого товара (если новый - -1)
      productId: -1,
      // Выбранный товар
      selectedProduct: {
        'category': '',
        'name': '',
        'description': '',
        'count': 0,
        'price': 0.0,
      },
      // Параметр отображения окна для добавления/редактирования товара
      dialog: false,
      // Список заголовков таблицы
      headers: [
        {
          title: 'Дата создания',
          key: 'created_at'
        },
        {
          title: 'Категория',
          key: 'category'
        },
        {
          title: 'Наименование',
          key: 'name'
        },
        {
          title: 'Описание',
          key: 'description'
        },
        {
          title: 'Количество',
          key: 'count'
        },
        {
          title: 'Цена',
          key: 'price'
        },
        {
          title: 'Действия',
          key: 'actions'
        },
      ]
    }
  },
  methods: {
    // Получение списка продуктов с backend
    async getProducts() {
      let productsRequest = await apiRequest(
        '/backend/api/v1/product/product',
        'GET',
        null
      )
      if (productsRequest.error) {
        showAlert(
          'error',
          'Товары',
          productsRequest.error
        )
      } else {
        this.piniaStore.setProducts(productsRequest.success)
        this.piniaStore.changeLoader(true)
      }
    },
    // Зафиксировать выбранный продукт для редактирования или добавление
    setProduct(product) {
      let prod = this.selectedProduct
      Object.keys(this.selectedProduct).map((key) => {
        if (product === null) {
          prod[key] = ''
        } else {
          prod[key] = product[key]
        }
      })
      this.selectedProduct = prod
    },
    // Сохранить информацию по товару
    async productSave() {
      let url = '/backend/api/v1/product/product/'
      let method = 'POST'
      if (this.productId !== -1) {
        url += this.productId+'/'
        method = 'PATCH'
      }
      let productSaveRequest = await apiRequest(
        url,
        method,
        this.selectedProduct
      )
      if (productSaveRequest.error) {
        showAlert(
          'error',
          'Товар',
          productSaveRequest.error
        )
      } else {
        showAlert(
          'success',
          'Товар',
          'Изменения успешно внесены'
        )
        this.getProducts()
      }
      this.dialog = !(this.dialog)
    },
    // Удалить объект
    async productDelete(product_id) {
      if (confirm('Вы уверены, что хотите удалить товар?')) {
        this.piniaStore.changeLoader()
        let productDeleteRequest = await apiRequest(
          '/backend/api/v1/product/product/'+product_id+'/',
          'DELETE',
          null
        )
        if (productDeleteRequest.error) {
          showAlert(
            'error',
            'Товары',
            productDeleteRequest.error
          )
          this.piniaStore.changeLoader(true)
        } else {
          showAlert(
            'success',
            'Товары',
            productDeleteRequest.success
          )
          this.getProducts()
        }
      }
    }
  },
  mounted() {
    this.getProducts()
  }
}

</script>

<style scoped lang="sass">

</style>
