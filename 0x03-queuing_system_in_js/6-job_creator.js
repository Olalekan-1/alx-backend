import kue from 'kue';

const queue = kue.createQueue();

const jobData = {
    phoneNumber: '1234567890',
    message: 'Hello, this is a notification message.'
};


const job = queue.create('push_notification_code', jobData);

job.on('complete', () => {
    console.log('Notification job completed');
});


job.on('failed', () => {
    console.log('Notification job failed');
});

job.save((err) => {
    if (err) {
        console.error(err);
        return;
    }
    console.log(`Notification job created: ${job.id}`);
});
