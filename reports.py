# %%
from pathlib import Path
import mne


sample_dir = Path(mne.datasets.sample.data_path())
raw_path = sample_dir / 'MEG' / 'sample' / 'sample_audvis_raw.fif'
report = mne.Report(title='My report')

# %% Load raw data
raw = (
    mne.io.read_raw_fif(raw_path)
    .pick_types(eeg=True, eog=True, stim=True)
    .crop(tmax=120)
    .load_data()
    .set_eeg_reference(ref_channels='average', projection=True)
)
report.add_raw(raw=raw, title='Input raw')

# %% Filter raw data
raw.filter(l_freq=1, h_freq=40)
report.add_raw(raw=raw, title='Filtered raw', psd=True)

# %% Create epochs
events = mne.find_events(raw, stim_channel='STI 014')
event_id = {
    'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3,
    'visual/right': 4, 'face': 5, 'buttonpress': 32
}
epochs = mne.Epochs(
    raw=raw,
    events=events,
    event_id=event_id,
    tmin=-0.2,
    tmax=0.5,
    baseline=(None, 0)
)
report.add_epochs(epochs=epochs, title='My epochs')


# %% Create evoked
evoked_auditory = epochs['auditory'].average()
report.add_evokeds(evokeds=evoked_auditory, titles='Auditory')

# %%
report.save('report.html')
