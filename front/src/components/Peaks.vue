<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Peaks</h1>
        <hr><br><br>
        <b-form @submit="getPeaks">
          <b-button type="submit" class="btn btn-success btn-sm">All Peaks</b-button>
        </b-form>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.peaks-in-bb-modal>
          Peaks In BoundingBox
        </button>
        <br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.add-peak-modal>
          Add Peak
        </button>
        <br>
        <alert :message=message v-if="showMessage"></alert>
        <br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Altitude</th>
              <th scope="col">Position</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(peak, index) in peaks" :key="index">
              <td>{{ peak.name }}</td>
              <td>{{ peak.altitude }}</td>
              <td>{{ peak.position }}</td>
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

    <b-modal ref="peakInBbModal"
            id="peaks-in-bb-modal"
            title="Get all peaks in bounding box"
            hide-footer>
      <b-form @submit="onSubmitPeaksInBb" @reset="onResetPeaksInBb" class="w-100">
      <b-form-group id="form-bottomleft-group"
                    label="Bottom-left:"
                    label-for="form-bottomleft-input">
          <b-form-input id="form-bottomleft-input"
                        type="text"
                        v-model="peaksInBbForm.bottomleft"
                        required
                        placeholder="Bottom left point [lon lat]">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-upperright-group"
                    label="Upper right:"
                    label-for="form-upperright-input">
          <b-form-input id="form-upperright-input"
                        type="text"
                        v-model="peaksInBbForm.upperright"
                        required
                        placeholder="Upper right point [lon lat]">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

    <b-modal ref="addPeakModal"
            id="add-peak-modal"
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
        <b-form-group id="form-position-group"
                    label="Position:"
                    label-for="form-position-input">
          <b-form-input id="form-position-input"
                        type="text"
                        v-model="addPeakForm.position"
                        required
                        placeholder="Enter position (geojson)">
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
        <b-form-group id="form-position-edit-group"
                    label="Position:"
                    label-for="form-position-edit-input">
          <b-form-input id="form-position-edit-input"
                        type="text"
                        v-model="editForm.position"
                        required
                        placeholder="Enter position">
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
        position: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        name: '',
        altitude: '',
        position: '',
      },
      peaksInBbForm: {
        bottomleft: '',
        upperright: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getPeaks() {
      const path = `${process.env.VUE_APP_BACKEND_URL}/peaks/peaks`;
      axios.get(path)
        .then((res) => {
          this.peaks = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getPeaksInBb(payload) {
      const path = `${process.env.VUE_APP_BACKEND_URL}/peaks/peaks/${payload.bottomleft}/${payload.upperright}`;
      axios.get(path)
        .then((res) => {
          this.peaks = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addPeak(payload) {
      const path = `${process.env.VUE_APP_BACKEND_URL}/peaks/peaks`;
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
      this.addPeakForm.position = '';
      this.editForm.id = '';
      this.editForm.name = '';
      this.editForm.altitude = '';
      this.editForm.position = '';
    },
    onSubmitPeaksInBb(evt) {
      evt.preventDefault();
      this.$refs.peakInBbModal.hide();
      const payload = {
        bottomleft: this.peaksInBbForm.bottomleft,
        upperright: this.peaksInBbForm.upperright,
      };
      this.getPeaksInBb(payload);
      this.initForm();
    },
    onResetPeaksInBb(evt) {
      evt.preventDefault();
      this.$refs.peakInBbModal.hide();
      this.initForm();
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addPeakModal.hide();
      const payload = {
        name: this.addPeakForm.name,
        altitude: this.addPeakForm.altitude,
        position: this.addPeakForm.position,
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
        position: this.editForm.position,
      };
      this.updatePeak(payload, this.editForm.id);
    },
    updatePeak(payload, peakID) {
      const path = `${process.env.VUE_APP_BACKEND_URL}/peaks/peaks/${peakID}`;
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
      this.getPeaks();
    },
    removePeak(peakID) {
      const path = `${process.env.VUE_APP_BACKEND_URL}/peaks/peaks/${peakID}`;
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
