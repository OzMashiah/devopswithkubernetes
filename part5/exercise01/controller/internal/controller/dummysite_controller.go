/*
Copyright 2025.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package controller

import (
	"context"
	"io/ioutil"
	"net/http"

	"github.com/go-logr/logr"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
	"sigs.k8s.io/controller-runtime/pkg/reconcile"

	part5dwkv1 "part5.dwk/api/v1"
)

// DummySiteReconciler reconciles a DummySite object
type DummySiteReconciler struct {
	client.Client
	Log    logr.Logger
	Scheme *runtime.Scheme
}

// +kubebuilder:rbac:groups=part5.dwk.part5.dwk,resources=dummysites,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=part5.dwk.part5.dwk,resources=dummysites/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=part5.dwk.part5.dwk,resources=dummysites/finalizers,verbs=update

// Reconcile is part of the main kubernetes reconciliation loop which aims to
// move the current state of the cluster closer to the desired state.
// TODO(user): Modify the Reconcile function to compare the state specified by
// the DummySite object against the actual cluster state, and then
// perform operations to make the cluster state reflect the state specified by
// the user.
//
// For more details, check Reconcile and its Result here:
// - https://pkg.go.dev/sigs.k8s.io/controller-runtime@v0.19.1/pkg/reconcile
func (r *DummySiteReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	// Fetch the DummySite instance
	var dummySite part5dwkv1.DummySite
	if err := r.Get(ctx, req.NamespacedName, &dummySite); err != nil {
		r.Log.Error(err, "unable to fetch DummySite")
		return reconcile.Result{}, client.IgnoreNotFound(err)
	}

	// Fetch website content from the specified URL
	content, err := fetchWebsiteContent(dummySite.Spec.WebsiteURL)
	if err != nil {
		r.Log.Error(err, "unable to fetch website content", "url", dummySite.Spec.WebsiteURL)
		return reconcile.Result{}, err
	}

	// Create the resources required to render the HTML (e.g., ConfigMap)
	err = r.createHTMLPage(ctx, &dummySite, content)
	if err != nil {
		r.Log.Error(err, "unable to create HTML page")
		return reconcile.Result{}, err
	}

	// Update DummySite status
	dummySite.Status.ContentFetched = true
	if err := r.Status().Update(ctx, &dummySite); err != nil {
		r.Log.Error(err, "unable to update DummySite status")
		return reconcile.Result{}, err
	}

	return reconcile.Result{}, nil
}

func fetchWebsiteContent(url string) (string, error) {
	resp, err := http.Get(url)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	return string(body), nil
}

func (r *DummySiteReconciler) createHTMLPage(ctx context.Context, dummySite *part5dwkv1.DummySite, content string) error {
	cm := &corev1.ConfigMap{
		ObjectMeta: metav1.ObjectMeta{
			Name:      dummySite.Name + "-html",
			Namespace: dummySite.Namespace,
		},
		Data: map[string]string{
			"index.html": content,
		},
	}
	// Set DummySite as the owner of the ConfigMap
	if err := controllerutil.SetControllerReference(dummySite, cm, r.Scheme); err != nil {
		return err
	}

	// Create ConfigMap
	return r.Create(ctx, cm)
}

// SetupWithManager sets up the controller with the Manager.
func (r *DummySiteReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&part5dwkv1.DummySite{}).
		Owns(&corev1.ConfigMap{}).
		Named("dummysite").
		Complete(r)
}
