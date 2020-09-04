import dlib
import imutils
import cv2
import time
import threading



class camCapture(object):
    def __init__(self, is_write=False, URL=None, save_path=None):
        self.writer = None
        self.URL = URL
        self.Frame = []
        self.status = False
        self.isstop = False


        if URL is None:
            self.capture = cv2.VideoCapture(0)
        else:
            self.capture = cv2.VideoCapture(URL)

        self.size = (int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                     int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        if is_write:
            fourcc = cv2.VideoWriter_fourcc(*'divx')

            if save_path is None:
                save_path = 'demo.avi'

            self.writer = cv2.VideoWriter(save_path, fourcc, 40, self.size)


    def sup_thread_start(self):
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def sub_thread_stop(self):
        self.isstop = True
        print('StreamStop')

    def get_frame(self):
        return self.Frame

    def queryframe(self):


        frame_count = 0
        FPS= "0"
        detector = dlib.get_frontal_face_detector()

        while not self.isstop:
            self.status, self.Frame = self.capture.read()


            if self.status is True:
                if frame_count == 0:
                    t_start=  time.time()
                frame_count += 1
                if frame_count >= 10:
                    FPS = "FPS=%1f" % (10 / (time.time() - t_start))
                    frame_count = 0
                    self.img_process(detector, self.Frame, self.writer)
                cv2.putText(self.Frame, FPS, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
                cv2.imshow("demo", self.Frame)

                if self.writer is not None:
                    self.writer.write(self.Frame)


                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print('get image false')
                break



        self.capture.release()

        if self.writer is not None:
            self.writer.release()




    def img_process(self, detector, frame, writer):


        face_react, scores, idx = detector.run(frame, 0)
        for i, d in enumerate(face_react):
            x1 = d.left()
            y1 = d.top()
            x2 = d.right()
            y2 = d.bottom()

            text = "%2.2f(%d)" % (scores[i], idx[i])

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4, cv2.LINE_AA)

            cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
        writer.write(frame)

        cv2.imshow("Face Dectection", frame)





class MyThread(threading.Thread):
    def __init__(self, ):
        threading.Thread.__init__(self)

    def run(self):



