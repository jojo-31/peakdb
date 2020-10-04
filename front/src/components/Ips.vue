<template>
  <div class='container'>
    <div class='row'>
      <div class='col-sm-10'>
        <h1>Blacked IPs</h1>
        <hr />
        <br />
        <br />
        <button type='button' class='btn btn-success btn-sm' v-b-modal.login-modal>Login</button>
        <br />
        <alert :message='message' v-if='showMessage'></alert>
        <br />
        <table class='table table-hover'>
          <thead>
            <tr>
              <th scope='col'>IP</th>
              <th scope='col'>Date</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for='(entry, index) in ips' :key='index'>
              <td>{{ entry.ip }}</td>
              <td>{{ entry.date }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <b-modal ref='loginModal' id='login-modal' title='Log in' hide-footer>
      <b-form @submit='onSubmit' @reset='onReset' class='w-100'>
        <b-form-group id='form-login-group' label='Login:' label-for='form-login-input'>
          <b-form-input id='form-login-input' type='text' v-model='user.login'
          required>
          </b-form-input>
        </b-form-group>
        <b-form-group id='form-password-group' label='Password:' label-for='form-password-input'>
          <b-form-input
            id='form-password-input'
            type='text'
            v-model='user.password'
            required
            placeholder
          ></b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type='submit' variant='primary'>Submit</b-button>
          <b-button type='reset' variant='danger'>Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      ips: [],
      message: '',
      showMessage: false,
      user: {
        login: '',
        password: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getIps() {
      const path = `${process.env.VUE_APP_BACKEND_URL}/ips/ips/`;
      axios
        .get(path)
        .then((res) => {
          this.ips = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getIps();
  },
};
</script>
