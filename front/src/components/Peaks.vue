<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Peaks</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.peak-modal>Add Peak</button>
        <br>
        <alert :message=message v-if="showMessage"></alert>
        <br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Altitude</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(peak, index) in peaks" :key="index">
              <td>{{ peak.name }}</td>
              <td>{{ peak.altitude }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.peak-update-modal
                          @click="editPeak(peak)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeletePeak(peak)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addPeakModal"
            id="peak-modal"
            title="Add a new peak"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addPeakForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-altitude-group"
                      label="Altitude:"
                      label-for="form-altitude-input">
            <b-form-input id="form-altitude-input"
                          type="text"
                          v-model="addPeakForm.altitude"
                          required
                          placeholder="Enter altitude">
            </b-form-input>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editPeakModal"
            id="peak-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-name-edit-group"
                    label="Name:"
                    label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-altitude-edit-group"
                      label="Altitude:"
                      label-for="form-altitude-edit-input">
            <b-form-input id="form-altitude-edit-input"
                          type="text"
                          v-model="editForm.altitude"
                          required
                          placeholder="Enter altitude">
            </b-form-input>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
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
      peaks: [],
      addPeakForm: {
        name: '',
        altitude: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        name: '',
        altitude: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getPeaks() {
      const path = 'http://localhost:5000/peaks';
      axios.get(path)
        .then((res) => {
          this.peaks = res.data.peaks;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addPeak(payload) {
      const path = 'http://localhost:5000/peaks';
      axios.post(path, payload)
        .then(() => {
          this.getPeaks();
          this.message = 'Peak added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getPeaks();
        });
    },
    initForm() {
      this.addPeakForm.name = '';
      this.addPeakForm.altitude = '';
      this.editForm.id = '';
      this.editForm.name = '';
      this.editForm.altitude = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addPeakModal.hide();
      const payload = {
        name: this.addPeakForm.name,
        altitude: this.addPeakForm.altitude,
      };
      this.addPeak(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addPeakModal.hide();
      this.initForm();
    },
    editPeak(peak) {
      this.editForm = peak;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editPeakModal.hide();
      const payload = {
        id: this.editForm.id,
        name: this.editForm.name,
        altitude: this.editForm.altitude,
      };
      this.updatePeak(payload, this.editForm.id);
    },
    updatePeak(payload, peakID) {
      const path = `http://localhost:5000/peaks/${peakID}`;
      axios.put(path, payload)
        .then(() => {
          this.getPeaks();
          this.message = 'Peak updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getPeaks();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editPeakModal.hide();
      this.initForm();
      this.getPeaks(); // why?
    },
    removePeak(peakID) {
      const path = `http://localhost:5000/peaks/${peakID}`;
      axios.delete(path)
        .then(() => {
          this.getPeaks();
          this.message = 'Peak removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getPeaks();
        });
    },
    onDeletePeak(peak) {
      this.removePeak(peak.id);
    },
  },
  created() {
    this.getPeaks();
  },
};
</script>
